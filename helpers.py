from fastapi import HTTPException
from models import  User, Skill, Tool
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
