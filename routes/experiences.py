from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
import sqlalchemy
from database import get_db
from models import Experience, Skill, Tool, ExperienceSkillLink, ExperienceToolLink, User
from schemas import UserRead, ExperienceRead, SkillRead, ToolRead
from typing import List, Dict

router = APIRouter()

@router.get("/users/{user_id}/experiences")
def get_user_experiences(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    work_experience_full_details = []
    work_experience = db.query(Experience).filter(Experience.user_id == user_id).all()

    for experience in work_experience:
        skills = db.query(Skill).join(ExperienceSkillLink).filter(ExperienceSkillLink.experience_id == experience.experience_id).all()
        tools = db.query(Tool).join(ExperienceToolLink).filter(ExperienceToolLink.experience_id == experience.experience_id).all()

        #Convert skill and tool records to Pydantic models
        skill_models = []
        for skill in skills:
            skill_model = SkillRead(skill_id=skill.skill_id, skill_name=skill.skill_name)
            skill_models.append(skill_model)

        tool_models = []
        for tool in tools:
            tool_model = ToolRead(tool_id=tool.tool_id, tool_name=tool.tool_name)
            tool_models.append(tool_model)

        #Add the experience with its skills and tools to the details list
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

    return work_experience_full_details


