import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import  Base
from initial_data import initialise_db
from models import Experience, Skill, ExperienceSkillLink, User, Tool, ExperienceToolLink, UserToolLink, UserSkillLink
from security import create_access_token
from passlib.context import CryptContext
import os
import logging
from datetime import datetime, timedelta
from jose import jwt

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


print(SECRET_KEY)
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY environment variable not set")


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


logging.basicConfig(level=logging.INFO)


@pytest.fixture(scope="function")
def test_db_session():
    logging.info("creating test database session")
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)

    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db_session = TestingSessionLocal()

    yield db_session 

    db_session.close()
    Base.metadata.drop_all(bind=engine)
    logging.info("test database session closed and tables dropped")



@pytest.fixture(scope="function")
def experience_with_skills(test_db_session):
    user = User(
        firstname="Jack", 
        lastname="Dimon", 
        email="jack@example.com", 
        hashed_password="hashed_pwdwxwx"
    )
    test_db_session.add(user)
    test_db_session.commit()

    experience = Experience(
        position="Software Engineer",
        company="SoftTech",
        industry="Information Technology",
        duration="01/01/2020 - 01/01/2024",
        description="Developing and maintaining mobile applications.",
        outcomes="Improved system performance by 50%",
        user_id=user.user_id  
    )  
    test_db_session.add(experience)
    test_db_session.commit()

    skill = Skill(skill_name="Communication")
    test_db_session.add(skill)
    test_db_session.commit()

    link = ExperienceSkillLink(experience_id=experience.experience_id, skill_id=skill.skill_id)
    test_db_session.add(link)
    test_db_session.commit()

    return experience.experience_id


@pytest.fixture(scope="function")
def experience_with_tools(test_db_session):
    user = User(
        firstname="Jack",
        lastname="Dimon",
        email="jack@example.com",
        hashed_password="hashed_pwd"
    )

    test_db_session.add(user)
    test_db_session.commit()

    experience = Experience(
        position="Software Engineer",
        company="SoftTech",
        industry="Information Technology",
        duration="01/01/2020 - 01/01/2024",
        description="Developing and maintaining mobile applications.",
        outcomes="Improved system performance by 50%",
        user_id=user.user_id  
    )

    test_db_session.add(experience)
    test_db_session.commit()

    tool = Tool(tool_name="React")
    test_db_session.add(tool)
    test_db_session.commit()

    link = ExperienceToolLink(experience_id=experience.experience_id, tool_id=tool.tool_id)
    test_db_session.add(link)
    test_db_session.commit()

    return experience.experience_id


@pytest.fixture(scope="function")
def experience_with_multiple_skills(test_db_session):
    user = User(
        firstname="Jack", 
        lastname="Dimon", 
        email="jack@example.com", 
        hashed_password="hashed_pwd"
    )
    test_db_session.add(user)
    test_db_session.commit()

    experience = Experience(
        position="Software Engineer",
        company="SoftTech",
        industry="Information Technology",
        duration="01/01/2020 - 01/01/2024",
        description="Developing and maintaining mobile applications.",
        outcomes="Improved system performance by 50%",
        user_id=user.user_id 
    )  
    test_db_session.add(experience)
    test_db_session.commit()

    skills = [
        Skill(skill_name="Communication"), 
        Skill(skill_name="Teamwork"),
        Skill(skill_name="Initiative")
    ]
    test_db_session.add_all(skills)
    test_db_session.commit()

    for skill in skills:
        link = ExperienceSkillLink(experience_id=experience.experience_id, skill_id=skill.skill_id)
        test_db_session.add(link)
    
    test_db_session.commit()

    return experience.experience_id



@pytest.fixture(scope="function")
def experience_with_multiple_tools(test_db_session):
    user = User(
        firstname="Jack", 
        lastname="Dimon", 
        email="jack@example.com", 
        hashed_password="hashed_pwd"
    )
    test_db_session.add(user)
    test_db_session.commit()

    experience = Experience(
        position="Software Engineer",
        company="SoftTech",
        industry="Information Technology",
        duration="01/01/2020 - 01/01/2024",
        description="Developing and maintaining mobile applications.",
        outcomes="Improved system performance by 50%",
        user_id=user.user_id 
    )  
    test_db_session.add(experience)
    test_db_session.commit()

    tools = [
        Tool(tool_name="React"),
        Tool(tool_name="PHP"),
        Tool(tool_name="AWS")
    ]

    test_db_session.add_all(tools)
    test_db_session.commit()

    for tool in tools:
        link = ExperienceToolLink(experience_id=experience.experience_id, tool_id=tool.tool_id)
        test_db_session.add(link)
    test_db_session.commit()

    return experience.experience_id


@pytest.fixture(scope="function")
def experience_with_zero_skills_and_tools(test_db_session):
    user = User(
        firstname="Jack", 
        lastname="Dimon", 
        email="jack@example.com", 
        hashed_password="hashed_pwd"
    )
    test_db_session.add(user)
    test_db_session.commit()

    experience = Experience(
        position="Software Engineer",
        company="SoftTech",
        industry="Information Technology",
        duration="01/01/2020 - 01/01/2024",
        description="Developing and maintaining mobile applications.",
        outcomes="Improved system performance by 50%",
        user_id=user.user_id 
    )  
    test_db_session.add(experience)
    test_db_session.commit()

    return experience.experience_id


@pytest.fixture(scope="function")
def test_user(test_db_session):
    logging.info("creating the user fixure")

    plain_password = 'plainpassword'
    hashed_password = pwd_context.hash(plain_password)
    test_user = User(
        firstname="Jack", 
        lastname="Dimon", 
        email="jack@example.com", 
        hashed_password=f'{hashed_password}'
    )

    test_db_session.add(test_user)
    test_db_session.commit()
    logging.info("commited user fixture to test_db_session")
    return test_user


@pytest.fixture(scope="function")
def test_experience(test_db_session, test_user):

 

    test_db_session.add(test_user)
    test_db_session.commit()
    experience = Experience(
        position="Software Engineer",
        company="SoftTech",
        industry="Information Technology",
        duration="01/01/2020 - 01/01/2024",
        description="Developing and maintaining mobile applications.",
        outcomes="Improved system performance by 50%",
        user_id=test_user.user_id 
    )  
    test_db_session.add(experience)
    test_db_session.commit()
    return experience

