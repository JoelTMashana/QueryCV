from typing import List
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from database import get_db
from models import User, Skill, UserSkillLink, Tool, UserToolLink
from schemas import UserRead, UserCreate, UserBase, UserLogin, UserSkills, UserTools, TokenResponse
from passlib.context import CryptContext
from security import verify_password, create_access_token


router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.get("/api/v1/users", response_model=List[UserRead]) # Only admin should be able to acess this route
async def read_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users



@router.post("/api/v1/users/register_user")
def create_user(user: UserCreate,  response: Response, db: Session = Depends(get_db)):
    try:
        db_user = db.query(User).filter(User.email == user.email).first()
        if db_user:
            raise HTTPException(status_code=400, detail="Email already exists.")

        hashed_password = pwd_context.hash(user.password)
        db_user = User(
            firstname=user.firstname,
            lastname=user.lastname,
            email=user.email,
            hashed_password=hashed_password
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        access_token = create_access_token(data={"sub": db_user.email})
        
        # HttpOnly cookie
        response.set_cookie(key="access_token", value=access_token, httponly=True, samesite='Lax')

        return {"message": "User registered successfully."}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error")


@router.post("/api/v1/login")
def login_route(user_credentials: UserLogin, response: Response, db: Session = Depends(get_db)):
    return login(user_credentials, response, db)

def login(user_credentials: UserLogin, response: Response, db: Session):
    user = db.query(User).filter(User.email == user_credentials.email).first()

    if not user or not verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email address or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": str(user.user_id)})
    response.set_cookie(key="access_token", value=access_token, httponly=True, samesite='Lax')

    return {"message": "User logged in successfully."}

@router.post("/api/v1/logout")
def logout(response: Response):
    response.delete_cookie(key="access_token")  
    return {"message": "User logged out successfully."}

@router.post("/api/v1/users/{user_id}/skills")
def link_skills_to_user(user_id: int, skills_selected_by_user: UserSkills, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.user_id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    for selected_skill_id in skills_selected_by_user.skill_ids:
        db_skill = db.query(Skill).filter(Skill.skill_id == selected_skill_id).first()
        if not db_skill:
            raise HTTPException(status_code=404, detail=f"Skill ID {selected_skill_id} not found")

        existing_link = db.query(UserSkillLink).filter_by(user_id=user_id, skill_id=selected_skill_id).first()
        if not existing_link:
            db_user_skill = UserSkillLink(user_id=user_id, skill_id=selected_skill_id)
            db.add(db_user_skill)

    db.commit()
    return {"message": "Skills linked to user successfully"}


@router.post("/api/v1/users/{user_id}/tools")
def link_tools_to_user(user_id: int, tools_selected_by_user: UserTools, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.user_id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    for selected_tool_id in tools_selected_by_user.tool_ids:
        db_tool = db.query(Tool).filter(Tool.tool_id == selected_tool_id).first()
        if not db_tool:
            raise HTTPException(status_code=404, detail=f"Tool ID {selected_tool_id} not found")

        existing_link = db.query(UserToolLink).filter_by(user_id=user_id, tool_id=selected_tool_id).first()
        if not existing_link:
            db_user_tool = UserToolLink(user_id=user_id, tool_id=selected_tool_id)
            db.add(db_user_tool)

    db.commit()
    return {"message": "Tools linked to user successfully"}