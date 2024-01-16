from services import get_skills_related_to_experience



def test_get_skills_related_to_experience_with_skills(experience_with_skills, test_db_session):
    # Arrange
    experience_id = experience_with_skills
    # Act
    result = get_skills_related_to_experience(experience_id, test_db_session)
    # Assert
    assert len(result) == 1  
    assert result[0].skill_id == 1 
    assert result[0].skill_name == "Communication"  

  
