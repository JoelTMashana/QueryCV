from fastapi.testclient import TestClient
from main import app  
from models import Skill, UserSkillLink, Tool, UserToolLink, ExperienceToolLink, ExperienceSkillLink, Experience
from schemas import UserSkills, UserTools, ToolLink, SkillLink, ToolCreate, SkillCreate, ExperienceUpdate, UserAuth
from routes.users import link_skills_to_user, link_tools_to_user
from routes.experiences import (link_tools_to_experience, 
                                link_skills_to_experience, 
                                update_user_experience, 
                                delete_user_experience)
from routes.tools_and_skills import  create_tool, create_skill, get_all_tools, get_all_skills


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


def test_create_tool(test_db_session):
    tool = ToolCreate(tool_name="Angular")

    result = create_tool(tool=tool, db=test_db_session)

    assert result.tool_name == tool.tool_name
    assert result.tool_id is not None  
    db_tool = test_db_session.query(Tool).filter(Tool.tool_name == tool.tool_name).first()
    assert db_tool is not None
    assert db_tool.tool_name == tool.tool_name

def test_create_skill(test_db_session):
    skill = SkillCreate(skill_name="Data Analysis")

    result = create_skill(skill=skill, db=test_db_session)

    assert result.skill_name == skill.skill_name
    assert result.skill_id is not None  

    db_skill = test_db_session.query(Skill).filter(Skill.skill_name == skill.skill_name).first()
    assert db_skill is not None
    assert db_skill.skill_name == skill.skill_name


def test_update_user_experience(test_db_session, test_user, test_experience):
    current_user = UserAuth(
        user_id=test_user.user_id,
        firstname=test_user.firstname,
        lastname=test_user.lastname,
        email=test_user.email
    )

    updated_experience_data = ExperienceUpdate(
        position="New Position",
        company="New Company",
        industry="New Industry",
        duration="New Duration",
        description="New Description",
        outcomes="New Outcomes"
    )

    update_user_experience(
        experience_id=test_experience.experience_id,
        updated_experience=updated_experience_data,
        db=test_db_session,
        current_user=current_user
    )

    db_experience = test_db_session.query(Experience).filter(Experience.experience_id == test_experience.experience_id).first()

    assert db_experience.position == "New Position"
    assert db_experience.company == "New Company"
    assert db_experience.industry == "New Industry"
    assert db_experience.duration == "New Duration"
    assert db_experience.description == "New Description"
    assert db_experience.outcomes == "New Outcomes"


def test_delete_experience(test_db_session, test_user, experience_with_skills):

    current_user = UserAuth(
        user_id=test_user.user_id,
        firstname=test_user.firstname,
        lastname=test_user.lastname,
        email=test_user.email
    )

    response = delete_user_experience(experience_id=experience_with_skills, db=test_db_session, current_user=current_user)

    assert response == {"message": "Experience and associated skills and tools deleted successfully"}
    assert not test_db_session.query(Experience).filter(Experience.experience_id == experience_with_skills).first()
    assert not test_db_session.query(ExperienceSkillLink).filter(ExperienceSkillLink.experience_id == experience_with_skills).all()
    assert not test_db_session.query(ExperienceToolLink).filter(ExperienceToolLink.experience_id == experience_with_skills).all()


def test_get_all_tools(test_db_session):
    tool1 = Tool(tool_name="Tool 1")
    tool2 = Tool(tool_name="Tool 2")
    test_db_session.add(tool1)
    test_db_session.add(tool2)
    test_db_session.commit()

    tools = get_all_tools(db=test_db_session)

    assert len(tools) == 2
    assert tools[0].tool_name == "Tool 1"
    assert tools[1].tool_name == "Tool 2"

def test_get_all_skills(test_db_session):
    skill1 = Skill(skill_name="Skill 1")
    skill2 = Skill(skill_name="Skill 2")
    test_db_session.add(skill1)
    test_db_session.add(skill2)
    test_db_session.commit()

    skills = get_all_skills(db=test_db_session)

    assert len(skills) == 2
    assert skills[0].skill_name == "Skill 1"
    assert skills[1].skill_name == "Skill 2"
