from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import  Tool, Skill
from schemas import ToolCreate, ToolRead, SkillRead, SkillCreate

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

