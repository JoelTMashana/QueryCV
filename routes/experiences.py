from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from models import Experience
from schemas import ExperienceCreate
from services import format_experiences_for_gpt, query_gpt

router = APIRouter()

@router.post("/experiences/")
def create_experience(experience: ExperienceCreate, db: Session = Depends(get_db)):
    """
    This function posts a new experience to the database.
    """
    db_experience = Experience(
        position=experience.position,
        company=experience.company,
        industry=experience.industry,
        duration=experience.duration,
        skills=experience.skills,
        tools=experience.tools,
        outcomes=experience.outcomes
    )
    db.add(db_experience)
    db.commit()
    db.refresh(db_experience)
    return db_experience

@router.get("/experiences/")
def format_and_query_experiences(user_query: str = Query(None), company: str = None, db: Session = Depends(get_db)):
    """
    This function reads and indiviual company or all companies.
    """
    if company:
        experiences = db.query(Experience).filter(Experience.company == company).all()
    else:
        experiences = db.query(Experience).all()
    
    if experiences:
       formatted_experiences = format_experiences_for_gpt(experiences)
       gpt_response = query_gpt(formatted_experiences, user_query)
       return {"gpt_response": gpt_response}    
    else:
        raise HTTPException(status_code=404, detail="No experiences found")
