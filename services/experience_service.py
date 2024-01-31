# import openai
# import os
# from dotenv import load_dotenv
# from fastapi import Depends
# from models import Skill, Tool, ExperienceSkillLink, ExperienceToolLink, Experience
# from schemas import SkillRead, ToolRead, ExperienceRead
# from sqlalchemy.orm import Session
# from typing import List
# from sqlalchemy.exc import SQLAlchemyError
# from models import Skill, Tool, UserSkillLink, UserToolLink
# from database import get_db
# load_dotenv()
# openai.api_key = os.environ.get("OPENAI_API_KEY")

# class ExperienceService:
#     def __init__(self, db: Session):
#         self.db = db
#         self.experience_cache = {}

#     def get_formatted_work_experience(self, user_id: int):
#         if user_id in self.experience_cache:
#             return self.experience_cache[user_id]

#         experiences = self.db.query(Experience).filter(Experience.user_id == user_id).all()
#         formatted_experiences = [self._format_experience(exp) for exp in experiences]

#         self.experience_cache[user_id] = formatted_experiences
#         return formatted_experiences

#     def _format_experience(self, experience):
#         skill_models = self.get_skills_related_to_experience(experience.experience_id)
#         tool_models = self.get_tools_related_to_experience(experience.experience_id)

#         return ExperienceRead(
#             experience_id=experience.experience_id,
#             position=experience.position,
#             company=experience.company,
#             industry=experience.industry,
#             duration=experience.duration,
#             description=experience.description,
#             outcomes=experience.outcomes,
#             skills=skill_models,
#             tools=tool_models
#         )

#     def get_skills_related_to_experience(self, experience_id: int):
#         skills = self.db.query(Skill).join(ExperienceSkillLink).filter(ExperienceSkillLink.experience_id == experience_id).all()
#         return [SkillRead(skill_id=skill.skill_id, skill_name=skill.skill_name) for skill in skills]

#     def get_tools_related_to_experience(self, experience_id: int):
#         tools = self.db.query(Tool).join(ExperienceToolLink).filter(ExperienceToolLink.experience_id == experience_id).all()
#         return [ToolRead(tool_id=tool.tool_id, tool_name=tool.tool_name) for tool in tools]

