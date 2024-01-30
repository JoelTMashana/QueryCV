from pydantic import BaseModel, EmailStr
from typing import List
from typing import Optional

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

class UserAuth(UserBase):
    user_id: int



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

class ExperienceReturn(BaseModel):
    experience_id: int


class ExperienceUpdate(BaseModel):
    position: Optional[str]= None
    company: Optional[str] = None
    industry: Optional[str] = None
    duration: Optional[str] = None
    description: Optional[str] = None
    outcomes: Optional[str] = None


class SkillLink(BaseModel):
    skill_ids: List[int]

class ToolLink(BaseModel):
    tool_ids: List[int]


class UserSkills(BaseModel):
    skill_ids: List[int]

class UserTools(BaseModel):
    tool_ids: List[int]


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class PreRegistrationExperience(BaseModel):
    position: str
    company: str
    description: str

class UserQueryPreRegistration(BaseModel):
    query: str
    experiences: List[PreRegistrationExperience]