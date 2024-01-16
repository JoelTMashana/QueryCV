
import openai
import os
from dotenv import load_dotenv
from fastapi import HTTPException
from models import Skill, Tool, ExperienceSkillLink, ExperienceToolLink, User
from schemas import SkillRead, ToolRead
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy.exc import SQLAlchemyError




load_dotenv()
openai.api_key = os.environ.get("OPENAI_API_KEY")

def format_experiences_for_gpt(experiences) -> str:
    if not experiences:
        return "This user has no experience listed. Encourage them to update their information."
    counter = 0

    try:      
        formatted_text = ""
        for exp in experiences:
            counter += 1
            # Construct  names as a comma-separated string
            skill_names = ''
            for skill in exp.skills:
                if skill_names:
                    skill_names += ', '
                skill_names += skill.skill_name
            
            tool_names = ''
            for tool in exp.tools:
                if tool_names:
                    tool_names += ', '
                tool_names += tool.tool_name

            formatted_exp = f"""
                Experience: {counter} 
                Position: {exp.position},
                Company: {exp.company},
                Industry: {exp.industry}, 
                Duration: {exp.duration},
                Description: {exp.description},
                Outcomes: {exp.outcomes},
                Skills: {skill_names},
                Tools: {tool_names}
                ----\n"""
          
            formatted_text += formatted_exp
        print(formatted_text.strip())
        return formatted_text.strip()
    except Exception as e:
        print(f"An error occurred: {e}")
        return "Apologise to the user, an error has occured"


def query_gpt(formatted_experiences, user_query):
    """
    Sends a query to the OpenAI GPT API using the updated interface and returns the response.
    """
    prompt = f"User Work Experience:\n{formatted_experiences}\nUser Query: {user_query}\n"

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo", 
            messages=[
                {"role": "system", "content": "You are a helpful assistant. You focus on giving CV related advice only. When the user ask questions which are not relevant to their CV or a job they are applying for, you should give short responses reminding them that your focus is on helping them build a strong CV and land their dream job. You should always speak to the user as you are speaking to them directly, speech should feel conversational."},
                {"role": "user", "content": prompt}
            ]
        )
        print(response)
        gpt_response = response.choices[0].message.content
        return gpt_response
    except Exception as e:
        print(f"An error occurred: {e}")
        return None




def get_skills_related_to_experience(experience_id: int, db: Session) -> List[SkillRead]:
    try:
        skills = db.query(Skill).join(ExperienceSkillLink).filter(ExperienceSkillLink.experience_id == experience_id).all()
        skill_models = []
        for skill in skills:
            skill_model = SkillRead(skill_id=skill.skill_id, skill_name=skill.skill_name)
            skill_models.append(skill_model)
        return skill_models
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database error while retrieving skills: {e}")


def get_tools_related_to_experience(experience_id: int, db: Session) -> List[ToolRead]:
    try:
        tools = db.query(Tool).join(ExperienceToolLink).filter(ExperienceToolLink.experience_id == experience_id).all()
        tool_models = []
        for tool in tools:
            tool_model = ToolRead(tool_id=tool.tool_id, tool_name=tool.tool_name)
            tool_models.append(tool_model)
        return tool_models
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database error while retrieving tools: {e}")


