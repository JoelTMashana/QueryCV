from fastapi.testclient import TestClient
from main import app  
from models import User, Skill, UserSkillLink, Tool, UserToolLink, ExperienceToolLink, ExperienceSkillLink
from schemas import UserSkills, UserTools, ToolLink, SkillLink
from routes.users import link_skills_to_user, link_tools_to_user
from routes.experiences import link_tools_to_experience, link_skills_to_experience

client = TestClient(app)

def test_read_home():
    response = client.get("/api/v1")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"} 



def test_link_skills_to_user(test_user, test_db_session):
    test_db_session.add(test_user)
    test_db_session.commit()

    test_skill_one = Skill(skill_name="Communication")
    test_skill_two = Skill(skill_name="Teamwork")
    test_db_session.add(test_skill_one)
    test_db_session.add(test_skill_two)
    test_db_session.commit()

    skills = UserSkills(skill_ids=[test_skill_one.skill_id, test_skill_two.skill_id])
    result = link_skills_to_user(user_id=test_user.user_id, skills_selected_by_user=skills, db=test_db_session)

    linked_skills = test_db_session.query(UserSkillLink).filter(UserSkillLink.user_id == test_user.user_id).all()
    assert len(linked_skills) == 2
    assert result == {"message": "Skills linked to user successfully"}


def test_link_tools_to_user(test_user, test_db_session):
    test_db_session.add(test_user)
    test_db_session.commit()

    test_tool_one = Tool(tool_name="Python")
    test_tool_two = Tool(tool_name="JavaScript")
    test_db_session.add(test_tool_one)
    test_db_session.add(test_tool_two)
    test_db_session.commit()

    tools = UserTools(tool_ids=[test_tool_one.tool_id, test_tool_two.tool_id])
    result = link_tools_to_user(user_id=test_user.user_id, tools_selected_by_user=tools, db=test_db_session)

    linked_tools = test_db_session.query(UserToolLink).filter(UserToolLink.user_id == test_user.user_id).all()
    assert len(linked_tools) == 2
    assert result == {"message": "Tools linked to user successfully"}


def test_link_tools_to_experience(test_experience, test_db_session):

    test_tool_one = Tool(tool_name="React")
    test_tool_two = Tool(tool_name="Docker")
    test_db_session.add(test_tool_one)
    test_db_session.add(test_tool_two)
    test_db_session.commit()

    tools = ToolLink(tool_ids=[test_tool_one.tool_id, test_tool_two.tool_id])
    result = link_tools_to_experience(experience_id=test_experience.experience_id, tools_selected_by_user=tools, db=test_db_session)

    linked_tools = test_db_session.query(ExperienceToolLink).filter(ExperienceToolLink.experience_id == test_experience.experience_id).all()
    assert len(linked_tools) == 2
    assert result == {"message": "Tools linked to experience successfully"}

def test_link_skills_to_experience(test_experience, test_db_session):
    
    test_skill_one = Skill(skill_name="Communication")
    test_skill_two = Skill(skill_name="Machine Learning")
    test_db_session.add(test_skill_one)
    test_db_session.add(test_skill_two)
    test_db_session.commit()

    skills = SkillLink(skill_ids=[test_skill_one.skill_id, test_skill_two.skill_id])

    result = link_skills_to_experience(experience_id=test_experience.experience_id, skills_selected_by_user=skills, db=test_db_session)

    linked_skills = test_db_session.query(ExperienceSkillLink).filter(ExperienceSkillLink.experience_id == test_experience.experience_id).all()

    assert len(linked_skills) == 2 
    assert result == {"message": "Skills linked to experience successfully"}
