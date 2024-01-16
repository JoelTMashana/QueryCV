from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from database import get_db
from models import Experience
from schemas import ExperienceRead
from typing import List, Dict
from helpers import check_user_exits
from services import  get_skills_related_to_experience, get_tools_related_to_experience, format_experiences_for_gpt
router = APIRouter()

@router.get("/users/{user_id}/experiences")
def get_user_experiences(user_id: int, db: Session = Depends(get_db)):

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
    format_experiences_for_gpt(work_experience_full_details)
    return work_experience_full_details



