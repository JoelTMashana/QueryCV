from fastapi import FastAPI
from routes.experiences import router as experiences_router
from routes.home import router as home_router
import os

app = FastAPI()
app.include_router(experiences_router)
app.include_router(home_router)

