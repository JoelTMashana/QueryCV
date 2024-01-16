from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import UserRead 

router = APIRouter()

@router.get("/users", response_model=List[UserRead])
async def read_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users
