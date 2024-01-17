from fastapi import Depends, APIRouter, Query, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Experience, User, Tool, Skill
from schemas import ExperienceRead, ExperienceCreate, ToolCreate, ToolRead, SkillRead, SkillCreate
from helpers import check_user_exits
from services import  get_skills_related_to_experience, get_tools_related_to_experience, format_experiences_for_gpt, query_gpt
from security import get_current_user 
from schemas import UserAuth

router = APIRouter()

@router.post("/api/v1/tools", response_model=ToolRead)
def create_tool(tool: ToolCreate, db: Session = Depends(get_db)):

    db_tool = Tool(**tool.dict()) 
    
    db.add(db_tool)
    db.commit()
    db.refresh(db_tool)

    return db_tool


@router.post("/api/v1/skills", response_model=SkillRead)
def create_skill(skill: SkillCreate, db: Session = Depends(get_db)):

    db_skill = Skill(**skill.dict()) 
    
    db.add(db_skill)
    db.commit()
    db.refresh(db_skill)

    return db_skill

