
import openai
import os
from dotenv import load_dotenv
from fastapi import HTTPException
from models import Skill, Tool, ExperienceSkillLink, ExperienceToolLink, Experience
from schemas import SkillRead, ToolRead
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy.exc import SQLAlchemyError
from models import Skill, Tool, UserSkillLink, UserToolLink

load_dotenv()
openai.api_key = os.environ.get("OPENAI_API_KEY")

def format_experiences_for_gpt(experiences) -> str:
    if not experiences:
        return "This user has no experience listed. Encourage them to update their information."
    counter = 0

    try:      
        formatted_text = ""
        for experience in experiences:
            counter += 1
            # Construct  names as a comma-separated string
            skill_names = ''
            for skill in experience.skills:
                if skill_names:
                    skill_names += ', '
                skill_names += skill.skill_name
            
            tool_names = ''
            for tool in experience.tools:
                if tool_names:
                    tool_names += ', '
                tool_names += tool.tool_name

            formatted_experience = f"""
                Experience: {counter} 
                Position: {experience.position},
                Company: {experience.company},
                Industry: {experience.industry}, 
                Duration: {experience.duration},
                Description: {experience.description},
                Outcomes: {experience.outcomes},
                Skills: {skill_names},
                Tools: {tool_names}
                ----\n"""
          
            formatted_text += formatted_experience
        print(formatted_text.strip())
        return formatted_text.strip()
    except Exception as e:
        print(f"An error occurred: {e}")
        return "Apologise to the user, an error has occured"


def format_pre_registration_experiences_for_gpt(experiences: List[Experience]) -> str:
    formatted = ""
    for experience in experiences:
        formatted += f"Position: {experience.position}, Company: {experience.company}, Description: {experience.description}\n"
    return formatted


def query_gpt(formatted_experiences, user_query):
    """
    Sends a query to the OpenAI GPT API using the updated interface and returns the response.
    """
    prompt = f"""User Work Experience: {formatted_experiences}
                 User Query: {user_query}
             """

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
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error while retrieving skills")



def get_tools_related_to_experience(experience_id: int, db: Session) -> List[ToolRead]:
    try:
        tools = db.query(Tool).join(ExperienceToolLink).filter(ExperienceToolLink.experience_id == experience_id).all()
        tool_models = []
        for tool in tools:
            tool_model = ToolRead(tool_id=tool.tool_id, tool_name=tool.tool_name)
            tool_models.append(tool_model)
        return tool_models
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error while retrieving tools")



def determine_items_to_remove_and_add(updated_items, current_items):
    """
    Determines items to add and remove based on the updated and current sets.
    """
    updated_set = set(updated_items)
    current_set = set(current_items)

    items_to_add = updated_set - current_set
    items_to_remove = current_set - updated_set

    return items_to_add, items_to_remove



def add_items_to_link_table(item_ids, item_type, link_model, link_model_kwargs, db):
    """
    Adds items to a link table.

    :param item_ids: IDs of the itemsto add
    :param item_type: Type of the item
    :param link_model: The link table model
    :param link_model_kwargs: Additional keyword arguments.
    :param db: DB session.
    """
    for item_id in item_ids:
        key_name = 'skill_id' if item_type == 'skill' else 'tool_id'

        if item_type == 'skill':
            if not db.query(Skill).filter(Skill.skill_id == item_id).first():
                raise HTTPException(status_code=404, detail=f"Item ID {item_id} not found")
        else:
            if not db.query(Tool).filter(Tool.tool_id == item_id).first():  
                raise HTTPException(status_code=404, detail=f"Item ID {item_id} not found")
           
        link_instance = link_model(**link_model_kwargs, **{key_name: item_id})
        db.add(link_instance)

def remove_items_from_link_table(item_ids, item_type, link_model, link_model_kwargs, db):
    """
    Removes items from a link table.
    """
    for item_id in item_ids:
        key_name = 'skill_id' if item_type == 'skill' else 'tool_id'
        link_instance = db.query(link_model).filter_by(**link_model_kwargs, **{key_name: item_id}).first()
        if link_instance:
            db.delete(link_instance)



def update_experience_item_link(experience_id, updated_item_ids, item_type, link_model, db):
    
    if item_type == 'skill':
        current_item_ids = [link.skill_id for link in db.query(link_model).filter(link_model.experience_id == experience_id).all()]
    else:  
        current_item_ids = [link.tool_id for link in db.query(link_model).filter(link_model.experience_id == experience_id).all()]

    items_to_add, items_to_remove = determine_items_to_remove_and_add(updated_item_ids, current_item_ids)
    
    add_items_to_link_table(items_to_add, item_type, link_model, {'experience_id': experience_id}, db)
    remove_items_from_link_table(items_to_remove, item_type, link_model, {'experience_id': experience_id}, db)



def update_user_item_link(user_id, updated_item_ids, item_type, link_model, db):
    
    if item_type == 'skill':
        current_item_ids = [link.skill_id for link in db.query(UserSkillLink).filter(UserSkillLink.user_id == user_id).all()]
    else:  
        current_item_ids = [link.tool_id for link in db.query(UserToolLink).filter(UserToolLink.user_id == user_id).all()]

    items_to_add, items_to_remove = determine_items_to_remove_and_add(updated_item_ids, current_item_ids)

    add_items_to_link_table(items_to_add, item_type, link_model, {'user_id': user_id}, db)
    remove_items_from_link_table(items_to_remove, item_type, link_model, {'user_id': user_id}, db)


def aggregate_user_item_ids_across_all_experiences(current_user, item_type, db,):
    user_experience_ids = db.query(Experience.experience_id).filter(Experience.user_id == current_user.user_id).all()
    
    updated_experience_item_ids = []
    for exp_id in user_experience_ids:
        if item_type == 'skill': 
            for link in db.query(ExperienceSkillLink).filter(ExperienceSkillLink.experience_id == exp_id.experience_id).all():
                if link.skill_id not in updated_experience_item_ids:
                    updated_experience_item_ids.append(link.skill_id)
        else:
            for link in db.query(ExperienceToolLink).filter(ExperienceToolLink.experience_id == exp_id.experience_id).all():
                if link.tool_id not in updated_experience_item_ids:
                    updated_experience_item_ids.append(link.tool_id)
    return updated_experience_item_ids
