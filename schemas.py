from pydantic import BaseModel, EmailStr
from typing import List

class UserBase(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr

class UserCreate(UserBase):
    password: str # Extends UserBase, adding password in this case

class UserRead(UserBase):
    user_id: int

    class Config: # Allows for conversion with alchemy ORM models
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserAuth(BaseModel):
    email: EmailStr


class SkillBase(BaseModel):
    skill_name: str

class SkillCreate(SkillBase):
    pass

class SkillRead(SkillBase):
    skill_id: int
    class Config:
        orm_mode = True


class ToolBase(BaseModel):
    tool_name: str

class ToolCreate(ToolBase):
    pass

class ToolRead(ToolBase):
    tool_id: int
    class Config:
        orm_mode = True


class ExperienceBase(BaseModel):
    position: str
    company: str
    industry: str
    duration: str
    description: str
    outcomes: str

class ExperienceCreate(ExperienceBase):
    pass

class ExperienceRead(ExperienceBase):
    experience_id: int
    skills: List[SkillRead] = []
    tools: List[ToolRead] = []
    class Config:
        orm_mode = True
