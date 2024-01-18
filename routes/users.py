from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User, Skill, UserSkillLink
from schemas import UserRead, UserCreate, UserBase, UserLogin, UserAuth, UserSkills
from passlib.context import CryptContext
from security import verify_password, create_access_token, get_current_user
from pydantic import BaseModel

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.get("/api/v1/users", response_model=List[UserRead]) # Only admin should be able to acess this route
async def read_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


@router.post("/api/v1/users/register_user", response_model=UserBase)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

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

    return db_user

def login(user_credentials: UserLogin, db: Session):
    user = db.query(User).filter(User.email == user_credentials.email).first()

    if not user or not verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email address or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": str(user.user_id)})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/api/v1/login")
def login_route(user_credentials: UserLogin, db: Session = Depends(get_db)):
    return login(user_credentials, db)



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
