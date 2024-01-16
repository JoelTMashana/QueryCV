from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from database import get_db
from models import Experience, Skill, Tool, ExperienceSkillLink, ExperienceToolLink, User
from schemas import UserRead
from typing import List, Dict

router = APIRouter()

@router.get("/users/{user_id}/experiences")
def get_user_experiences(user_id: int, db: Session = Depends(get_db)):
    experiences = db.query(Experience).filter(Experience.user_id == user_id).all() # Get all experiences for user
    experience_details = []

    # Loops through the experiences, associates with skills and tools used then returns the result
    for experience in experiences:
        skills = db.query(Skill).join(ExperienceSkillLink).filter(ExperienceSkillLink.experience_id == experience.experience_id).all()
        tools = db.query(Tool).join(ExperienceToolLink).filter(ExperienceToolLink.experience_id == experience.experience_id).all()
        experience_details.append({
            "experience": experience,
            "skills": skills,
            "tools": tools
        })

    return experience_details


