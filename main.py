from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.experiences import router as experiences_router
from routes.home import router as home_router
from routes.users import router as user_router
from routes.tools_and_skills import router as tools_and_skills_router
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

origins = [
    "http://localhost:3000",
    "https://query-cv.vercel.app/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"], 
    allow_headers=["Content-Type", "Authorization"],  
)

app.include_router(experiences_router)
app.include_router(home_router)
app.include_router(user_router)
app.include_router(tools_and_skills_router)

