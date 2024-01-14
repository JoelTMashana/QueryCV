import uuid
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.sqlite import VARCHAR

Base = declarative_base()

class Experience(Base):
    __tablename__ = "experiences"

    id = Column(VARCHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    position = Column(String, index=True)
    company = Column(String, index=True)
    industry = Column(String, index=True)
    duration = Column(String, index=True)
    skills = Column(String, index=True)
    experience = Column(String, index=True)
    tools = Column(String, index=True)
    outcomes = Column(String, index=True)
