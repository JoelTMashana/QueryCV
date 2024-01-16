from fastapi import HTTPException
from models import  User
from sqlalchemy.orm import Session


def check_user_exits(user_id, db: Session):
    user = db.query(User).filter(User.user_id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
