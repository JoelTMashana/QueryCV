from pydantic import BaseModel, EmailStr


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




class ExperienceBase(BaseModel):
    position: str
    company: str
    industry: str
    duration: str
    description: str

class ExperienceCreate(BaseModel):
    position: str
    company: str
    industry: str
    duration: str
    description: str

class ExperienceRead(ExperienceBase):
    experience_id: int
    class Config:
        orm_mode = True
