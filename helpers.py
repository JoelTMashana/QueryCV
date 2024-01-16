from fastapi import HTTPException
from models import Skill, Tool, ExperienceSkillLink, ExperienceToolLink, User
from schemas import SkillRead, ToolRead
from sqlalchemy.orm import Session
from typing import List



def check_user_exits(user_id, db: Session):
    user = db.query(User).filter(User.user_id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

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