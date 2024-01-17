from fastapi import APIRouter

router = APIRouter()

@router.get("/api/v1/") # Need to protect this route if in use
def read_home():
    return {"message": "Hello World"} 