from fastapi import Depends, APIRouter, Query, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Experience, User, ExperienceSkillLink, Skill
from schemas import ExperienceRead, ExperienceCreate, SkillLink
from helpers import check_user_exits
from services import  get_skills_related_to_experience, get_tools_related_to_experience, format_experiences_for_gpt, query_gpt
from security import get_current_user 
from schemas import UserAuth
from typing import List
from pydantic import BaseModel
router = APIRouter()

@router.get("/api/v1/users/{user_id}/experiences")
def get_user_experiences(
    user_id: int, 
    user_query: str = Query(None), 
    db: Session = Depends(get_db),
    current_user: UserAuth = Depends(get_current_user)
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
def link_skills_to_experience(experience_id: int, skill_link: SkillLink, db: Session = Depends(get_db)):
    db_experience = db.query(Experience).filter(Experience.experience_id == experience_id).first()
    if not db_experience:
        raise HTTPException(status_code=404, detail="Experience not found")

    # Validate and link each skill ID
    for skill_id in skill_link.skill_ids:
        db_skill = db.query(Skill).filter(Skill.skill_id == skill_id).first()
        if not db_skill:
            raise HTTPException(status_code=404, detail=f"Skill ID {skill_id} not found")

        # Checks if the skill is already linked to the experience
        existing_link = db.query(ExperienceSkillLink).filter_by(experience_id=experience_id, skill_id=skill_id).first()
        if not existing_link:
            db_experience_skill = ExperienceSkillLink(experience_id=experience_id, skill_id=skill_id)
            db.add(db_experience_skill)
        else:
            return {"message": "Skills alreay linked to experience"}
    db.commit()
    return {"message": "Skills linked to experience successfully"}