from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from database import get_db
from models import  Tool, Skill
from schemas import ToolCreate, ToolRead, SkillRead, SkillCreate
from typing import List

router = APIRouter()

@router.post("/api/v1/tools", response_model=ToolRead)
def create_tool(tool: ToolCreate, db: Session = Depends(get_db)): # Admin
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
def create_skill(skill: SkillCreate, db: Session = Depends(get_db)): # Admin
    try:
        db_skill = Skill(**skill.dict()) 
        db.add(db_skill)
        db.commit()
        db.refresh(db_skill)
        return db_skill
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error")
    

@router.get("/api/v1/tools", response_model=List[ToolRead])
def get_all_tools(db: Session = Depends(get_db)):
    try:
        tools = db.query(Tool).all()
        return tools
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error")


@router.get("/api/v1/skills", response_model=List[SkillRead])
def get_all_skills(db: Session = Depends(get_db)):
    try:
        skills = db.query(Skill).all()
        return skills
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error")