from fastapi import Depends, APIRouter, Query, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Experience, User
from schemas import ExperienceRead, ExperienceCreate
from helpers import check_user_exits
from services import  get_skills_related_to_experience, get_tools_related_to_experience, format_experiences_for_gpt, query_gpt
from security import get_current_user 
from schemas import UserAuth

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




@router.post("/users/{user_id}/experiences", response_model=ExperienceCreate)
def create_experience_for_user(user_id: int, experience: ExperienceCreate, db: Session = Depends(get_db)):
     # Check if user exists
    db_user = db.query(User).filter(User.user_id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    db_experience = Experience(**experience.dict(), user_id=user_id) 
    
    db.add(db_experience)
    db.commit()
    db.refresh(db_experience)

    return db_experience

