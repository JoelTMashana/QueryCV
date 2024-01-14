from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def read_home():
    return {"message": "Hello World"} 