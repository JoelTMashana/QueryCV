from fastapi import APIRouter

router = APIRouter()

@router.get("/api/v1/")
def read_home():
    return {"message": "Hello World"} 