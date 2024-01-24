from fastapi import Depends, APIRouter, Query, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from database import get_db
from models import Experience, User, ExperienceSkillLink, Skill, Tool, ExperienceToolLink,  UserSkillLink, UserToolLink
from schemas import ExperienceRead, ExperienceCreate, SkillLink, ToolLink, ExperienceUpdate
from helpers import check_user_exits
from services import  (get_skills_related_to_experience, 
                       get_tools_related_to_experience, 
                       format_experiences_for_gpt, 
                       query_gpt, 
                       update_user_item_link, 
                       update_experience_item_link, 
                       aggregate_user_item_ids_across_all_experiences)
from security import get_current_user 
from schemas import UserAuth

router = APIRouter()

@router.get("/api/v1/users/{user_id}/experiences")
def get_user_experiences(
    user_id: int, 
    user_query: str = Query(None), 
    db: Session = Depends(get_db),
    current_user: UserAuth = Depends(get_current_user) # Must add to rest to place behind auth wall 
    ):

    check_user_exits(user_id, db)
    work_experience_full_details = []
    work_experience = db.query(Experience).filter(Experience.user_id == user_id).all()

    for experience in work_experience:
        skill_models = get_skills_related_to_experience(experience.experience_id, db)

        tool_models = get_tools_related_to_experience(experience.experience_id, db)

        experience_detail = ExperienceRead(
            experience_id=experience.experience_id,
            position=experience.position,
            company=experience.company,
            industry=experience.industry,
            duration=experience.duration,
            description=experience.description,
            outcomes=experience.outcomes,
            skills=skill_models,
            tools=tool_models
        )
        work_experience_full_details.append(experience_detail)
    formatted_experiences = format_experiences_for_gpt(work_experience_full_details)
    print(formatted_experiences)
    if not user_query:
        return {'response': 'User did not enter a query'}
    gpt_response = query_gpt(formatted_experiences, user_query)
    return {"gpt_response": gpt_response}


@router.post("/api/v1/users/{user_id}/experiences", response_model=ExperienceRead)
def create_experience_for_user(user_id: int, experience: ExperienceCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.user_id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    db_experience = Experience(**experience.dict(), user_id=user_id) 
    
    db.add(db_experience)
    db.commit()
    db.refresh(db_experience)

    return db_experience



@router.post("/api/v1/experiences/{experience_id}/skills")
def link_skills_to_experience(experience_id: int, skills_selected_by_user: SkillLink, db: Session = Depends(get_db)):
    db_experience = db.query(Experience).filter(Experience.experience_id == experience_id).first()
    if not db_experience:
        raise HTTPException(status_code=404, detail="Experience not found")

    for selected_skill_id in skills_selected_by_user.skill_ids:
        db_skill = db.query(Skill).filter(Skill.skill_id == selected_skill_id).first()
        if not db_skill:
            raise HTTPException(status_code=404, detail=f"Skill ID {selected_skill_id} not found")

        existing_link = db.query(ExperienceSkillLink).filter_by(experience_id=experience_id, skill_id=selected_skill_id).first()
        if not existing_link:
            db_experience_skill = ExperienceSkillLink(experience_id=experience_id, skill_id=selected_skill_id)
            db.add(db_experience_skill)
        else:
            return {"message": "Skills alreay linked to experience"}
    db.commit()
    return {"message": "Skills linked to experience successfully"}



@router.post("/api/v1/experiences/{experience_id}/tools")
def link_tools_to_experience(experience_id: int, tools_selected_by_user: ToolLink, db: Session = Depends(get_db)):
    db_experience = db.query(Experience).filter(Experience.experience_id == experience_id).first()
    if not db_experience:
        raise HTTPException(status_code=404, detail="Experience not found")

    for selected_tool_id in tools_selected_by_user.tool_ids:
        db_tool = db.query(Tool).filter(Tool.tool_id == selected_tool_id).first()
        if not db_tool:
            raise HTTPException(status_code=404, detail=f"Tool ID {selected_tool_id} not found")

        existing_link = db.query(ExperienceToolLink).filter_by(experience_id=experience_id, tool_id=selected_tool_id).first()
        if not existing_link:
            db_experience_tool = ExperienceToolLink(experience_id=experience_id, tool_id=selected_tool_id)
            db.add(db_experience_tool)
        else:
            return {"message": "Tool already linked to experience"}
    db.commit()
    return {"message": "Tools linked to experience successfully"}



@router.patch("/api/v1/experiences/{experience_id}")
def update_user_experience(experience_id: int, updated_experience: ExperienceUpdate, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    db_experience = db.query(Experience).filter(Experience.experience_id == experience_id).first()
    if not db_experience:
        raise HTTPException(status_code=404, detail="Experience not found")

    if db_experience.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not authorised to update this experience")

    for attritube, value in vars(updated_experience).items():
        if value is not None:
            setattr(db_experience, attritube, value)

    db.commit()
    return db_experience



@router.patch("/api/v1/experiences/{experience_id}/skills")
def update_skills_associated_with_user_and_experience(
    experience_id: int, 
    updated_skills: SkillLink, 
    db: Session = Depends(get_db), 
    current_user: UserAuth = Depends(get_current_user)
    ):

    try:         
        db_experience = db.query(Experience).filter(Experience.experience_id == experience_id).first()
        if not db_experience or db_experience.user_id != current_user.user_id:
            raise HTTPException(status_code=404, detail="Experience not found or not owned by user")

        # Update the Experience skill table to reflect changes
        update_experience_item_link(experience_id, updated_skills.skill_ids, 'skill', ExperienceSkillLink, db)

        db.flush() # Sychronise

        updated_experience_skill_ids = aggregate_user_item_ids_across_all_experiences(current_user, 'skill', db)           
        update_user_item_link(current_user.user_id, updated_experience_skill_ids, 'skill', UserSkillLink, db)    
        db.commit()
        return {"message": "Skills associated with experience updated successfully"}

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.patch("/api/v1/experiences/{experience_id}/tools")
def update_tools_associated_with_user_and_experience(
    experience_id: int, 
    updated_tools: ToolLink, 
    db: Session = Depends(get_db), 
    current_user: UserAuth = Depends(get_current_user)
):

    try:
        db_experience = db.query(Experience).filter(Experience.experience_id == experience_id).first()
        if not db_experience or db_experience.user_id != current_user.user_id:
            raise HTTPException(status_code=404, detail="Experience not found or not owned by user")

        update_experience_item_link(experience_id, updated_tools.tool_ids, 'tool', ExperienceToolLink, db)
        db.flush() 
        updated_experience_tool_ids = aggregate_user_item_ids_across_all_experiences(current_user, 'tool', db) 
        update_user_item_link(current_user.user_id, updated_experience_tool_ids, 'tool', UserToolLink, db)
        db.commit()
        return {"message": "Tools associated with experience updated successfully"}

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")





@router.delete("/api/v1/experiences/{experience_id}")
def delete_user_experience(experience_id: int, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    try:
        db_experience = db.query(Experience).filter(Experience.experience_id == experience_id).first()
        if not db_experience or db_experience.user_id != current_user.user_id:
            raise HTTPException(status_code=404, detail="Experience not found or not owned by user")

        db.query(ExperienceSkillLink).filter(ExperienceSkillLink.experience_id == experience_id).delete()
        db.query(ExperienceToolLink).filter(ExperienceToolLink.experience_id == experience_id).delete()

        db.delete(db_experience)

        updated_experience_skill_ids = aggregate_user_item_ids_across_all_experiences(current_user, 'skill', db)           
        update_user_item_link(current_user.user_id, updated_experience_skill_ids, 'skill', UserSkillLink, db) 

        updated_experience_tool_ids = aggregate_user_item_ids_across_all_experiences(current_user, 'tool', db) 
        update_user_item_link(current_user.user_id, updated_experience_tool_ids, 'tool', UserToolLink, db)

        db.commit()
        return {"message": "Experience and associated skills and tools deleted successfully"}

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

