from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from database import get_db
from models import  Tool, Skill
from schemas import ToolCreate, ToolRead, SkillRead, SkillCreate

router = APIRouter()

@router.post("/api/v1/tools", response_model=ToolRead)
def create_tool(tool: ToolCreate, db: Session = Depends(get_db)):
    try:
        db_tool = Tool(**tool.dict())
        db.add(db_tool)
        db.commit()
        db.refresh(db_tool)
        return db_tool
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error")

@router.post("/api/v1/skills", response_model=SkillRead)
def create_skill(skill: SkillCreate, db: Session = Depends(get_db)):
    try:
        db_skill = Skill(**skill.dict()) 
        db.add(db_skill)
        db.commit()
        db.refresh(db_skill)
        return db_skill
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error")