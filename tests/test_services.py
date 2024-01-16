from services import get_skills_related_to_experience, get_tools_related_to_experience



def test_get_skills_related_to_experience_with_skills(experience_with_skills, test_db_session):
    # Arrange
    experience_id = experience_with_skills
    # Act
    result = get_skills_related_to_experience(experience_id, test_db_session)
    # Assert
    assert len(result) == 1  
    assert result[0].skill_id == 1 
    assert result[0].skill_name == "Communication"  

  
  
def test_get_tools_related_to_experience_with_tools(experience_with_tools, test_db_session):
    
    experience_id = experience_with_tools

    result = get_tools_related_to_experience(experience_id, test_db_session)

    assert len(result) == 1  
    assert result[0].tool_id == 1 
    assert result[0].tool_name == "React"  
  

def test_get_skills_related_to_experience_with_multiple_skills(experience_with_multiple_skills, test_db_session):
    
    experience_id = experience_with_multiple_skills

    result = get_skills_related_to_experience(experience_id, test_db_session)

    assert len(result) == 3  

def test_get_tools_related_to_experience_with_multiple_tools(experience_with_multiple_tools, test_db_session):
    
    experience_id = experience_with_multiple_tools

    result = get_tools_related_to_experience(experience_id, test_db_session)

    assert len(result) == 3  


def test_get_skills_related_to_experience_with_zero_skills(experience_with_zero_skills, test_db_session):
    
    experience_id = experience_with_zero_skills

    result = get_skills_related_to_experience(experience_id, test_db_session)

    assert len(result) == 0  


  

