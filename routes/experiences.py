from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
import sqlalchemy
from database import get_db
from models import Experience, Skill, Tool, ExperienceSkillLink, ExperienceToolLink, User
from schemas import UserRead, ExperienceRead, SkillRead, ToolRead
from typing import List, Dict
from helpers import check_user_exits

router = APIRouter()



def get_skills_related_to_experience(experience_id: int, db: Session) -> List[SkillRead]:
    skills = db.query(Skill).join(ExperienceSkillLink).filter(ExperienceSkillLink.experience_id == experience_id).all()
    skill_models = []
    for skill in skills:
        skill_model = SkillRead(skill_id=skill.skill_id, skill_name=skill.skill_name)
        skill_models.append(skill_model)
    return skill_models


def get_tools_related_to_experience(experience_id: int, db: Session) -> List[ToolRead]:
    tools = db.query(Tool).join(ExperienceToolLink).filter(ExperienceToolLink.experience_id == experience_id).all()
    tool_models = []
    for tool in tools:
        tool_model = ToolRead(tool_id=tool.tool_id, tool_name=tool.tool_name)
        tool_models.append(tool_model)
    return tool_models


@router.get("/users/{user_id}/experiences")
def get_user_experiences(user_id: int, db: Session = Depends(get_db)):

    check_user_exits(user_id, db)

    work_experience_full_details = []
    work_experience = db.query(Experience).filter(Experience.user_id == user_id).all()

    for experience in work_experience:
        # skills = db.query(Skill).join(ExperienceSkillLink).filter(ExperienceSkillLink.experience_id == experience.experience_id).all()
        # tools = db.query(Tool).join(ExperienceToolLink).filter(ExperienceToolLink.experience_id == experience.experience_id).all()

        #Convert skill and tool records to Pydantic models
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

    return work_experience_full_details


