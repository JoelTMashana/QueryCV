import uuid
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.sqlite import VARCHAR
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String)
    lastname = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    # Relationships
    experiences = relationship("Experience", back_populates="owner")
    user_skills = relationship("UserSkillLink", back_populates="user")
    user_tools = relationship("UserToolLink", back_populates="user")


class Experience(Base):
    __tablename__ = 'experiences'
    experience_id = Column(Integer, primary_key=True, index=True)
    position = Column(String)
    company = Column(String)
    industry = Column(String)
    duration = Column(String)
    description = Column(String)
    outcomes = Column(String)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    owner = relationship("User", back_populates="experiences")
    experience_skills = relationship('ExperienceSkillLink', back_populates='experience')
    experience_tools = relationship('ExperienceToolLink', back_populates='experience')


class Skill(Base):
    __tablename__ = 'skills'
    skill_id = Column(Integer, primary_key=True, index=True)
    skill_name = Column(String(35), index=True)
    user_skills = relationship('UserSkillLink', back_populates='skill')
    experience_skills = relationship('ExperienceSkillLink', back_populates='skill')


class Tool(Base):
    __tablename__ = 'tools'
    tool_id = Column(Integer, primary_key=True, index=True)
    tool_name = Column(String(35), index=True)
    user_tools = relationship('UserToolLink', back_populates='tool')
    experience_tools = relationship('ExperienceToolLink', back_populates='tool')


class UserSkillLink(Base):
    __tablename__ = 'user_skills_link'
    user_skill_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), index=True)
    skill_id = Column(Integer, ForeignKey('skills.skill_id'), index=True)
    user = relationship('User', back_populates='user_skills')
    skill = relationship('Skill', back_populates='user_skills')


class UserToolLink(Base):
    __tablename__ = 'user_tools_link'
    user_tool_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), index=True)
    tool_id = Column(Integer, ForeignKey('tools.tool_id'), index=True)
    user = relationship('User', back_populates='user_tools')
    tool = relationship('Tool', back_populates='user_tools')


class ExperienceSkillLink(Base):
    __tablename__ = 'experience_skills_link'
    experience_skill_id = Column(Integer, primary_key=True, index=True)
    experience_id = Column(Integer, ForeignKey('experiences.experience_id'), index=True)
    skill_id = Column(Integer, ForeignKey('skills.skill_id'), index=True)
    # Relationships
    experience = relationship('Experience', back_populates='experience_skills')
    skill = relationship('Skill', back_populates='experience_skills')
    experience = relationship('Experience', back_populates='experience_skills')


class ExperienceToolLink(Base):
    __tablename__ = 'experience_tools_link'
    experience_tool_id = Column(Integer, primary_key=True, index=True)
    experience_id = Column(Integer, ForeignKey('experiences.experience_id'), index=True)
    tool_id = Column(Integer, ForeignKey('tools.tool_id'), index=True)
    # Relationships
    experience = relationship('Experience', back_populates='experience_tools')
    tool = relationship('Tool', back_populates='experience_tools')
    experience = relationship('Experience', back_populates='experience_tools')

