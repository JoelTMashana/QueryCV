from fastapi import FastAPI
from routes.experiences import router as experiences_router
import os

app = FastAPI()
app.include_router(experiences_router)

