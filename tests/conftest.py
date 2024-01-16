import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import  Base
from initial_data import initialise_db
from models import Experience, Skill, ExperienceSkillLink, User



@pytest.fixture(scope="function")
def test_db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)

    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db_session = TestingSessionLocal()

    yield db_session 

    db_session.close()
    Base.metadata.drop_all(bind=engine)



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
