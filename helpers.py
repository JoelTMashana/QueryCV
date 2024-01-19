from fastapi import HTTPException
from models import  User
from sqlalchemy.orm import Session


def check_user_exits(user_id, db: Session):
    user = db.query(User).filter(User.user_id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")



def determine_items_to_remove_and_add(updated_items, current_items):
    """
    Determines items to add and remove based on the updated and current sets.
    """
    updated_set = set(updated_items)
    current_set = set(current_items)

    items_to_add = updated_set - current_set
    items_to_remove = current_set - updated_set

    return items_to_add, items_to_remove