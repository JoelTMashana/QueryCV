from pydantic import BaseModel

class ExperienceCreate(BaseModel):
    position: str
    company: str
    industry: str
    duration: str
    skills: str
    experience: str
    tools: str
    outcomes: str