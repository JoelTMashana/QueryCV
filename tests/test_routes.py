from fastapi.testclient import TestClient
from main import app  
from models import User, Skill, UserSkillLink
from schemas import UserSkills
from routes.users import link_skills_to_user


client = TestClient(app)

def test_read_home():
    response = client.get("/api/v1")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"} 



def test_link_skills_to_user(test_db_session):
    test_user = User(firstname="Test", lastname="User", email="test@example.com", hashed_password="hashed_test")
    test_db_session.add(test_user)
    test_db_session.commit()

    test_skill_one = Skill(skill_name="Python")
    test_skill_two = Skill(skill_name="JavaScript")
    test_db_session.add(test_skill_one)
    test_db_session.add(test_skill_two)
    test_db_session.commit()

    skills = UserSkills(skill_ids=[test_skill_one.skill_id, test_skill_two.skill_id])

    response = link_skills_to_user(user_id=test_user.user_id, skills_selected_by_user=skills, db=test_db_session)

    linked_skills = test_db_session.query(UserSkillLink).filter(UserSkillLink.user_id == test_user.user_id).all()
    assert len(linked_skills) == 2
    assert response == {"message": "Skills linked to user successfully"}
