from sqlalchemy.orm import Session
from models import Experience, Skill, Tool, User, UserSkillLink, UserToolLink, ExperienceSkillLink, ExperienceToolLink
import logging

def initialise_db(engine):
    """
    Initialises the database with predefined data if the database is empty
    """
    db = Session(bind=engine)
    print('Initialise DB called')
    try:
        if db.query(User).count() == 0:
            # Adds initial users
            initial_users = [
                User(firstname="John", lastname="Doe", email="john@example.com", hashed_password="hashed_pwd"),
                
            ]
            db.add_all(initial_users)

        if db.query(Skill).count() == 0:
            initial_skills = [
                Skill(skill_name="Communication"),
            ]
            db.add_all(initial_skills)

        if db.query(Tool).count() == 0:
            initial_tools = [
                Tool(tool_name="React"),
            ]
            db.add_all(initial_tools)

        if db.query(Experience).count() == 0:
            initial_experiences = [
                Experience(
                    position="Software Developer",
                    company="TechCorp",
                    industry="Information Technology",
                    duration="01/01/2020 - 01/01/2023",
                    description="Developing and maintaining web applications.",
                    outcomes="Improved system performance by 20%",
                    user_id=1  
                ),       
            ]

            db.add_all(initial_experiences)
        
        if db.query(UserSkillLink).count() == 0:
            intial_user_skills_link = [
                UserSkillLink(
                    user_id=1,
                    skill_id=1
                )            
            ]
            db.add_all(intial_user_skills_link)

        if db.query(UserToolLink).count() == 0:
            intial_user_tools_link = [
                UserToolLink(
                    user_id=1,
                    tool_id=1
                )            
            ]
            db.add_all(intial_user_tools_link)

        if db.query(UserToolLink).count() == 0:
            intial_user_tools_link = [
                UserToolLink(
                    user_id=1,
                    tool_id=1
                )            
            ]
            db.add_all(intial_user_tools_link)

        if db.query(ExperienceSkillLink).count() == 0:
            intial_experience_skills_link = [
                ExperienceSkillLink(
                    experience_id=1,
                    skill_id=1
                )            
            ]
            db.add_all(intial_experience_skills_link)

        if db.query(ExperienceToolLink).count() == 0:
            intial_experience_tools_link = [
                ExperienceToolLink(
                    experience_id=1,
                    tool_id=1
                )            
            ]
            db.add_all(intial_experience_tools_link)



        db.commit()
        logging.info("Database initialised with predefined data.")
    except Exception as e:
        logging.error(f"Error initialising database: {e}")
    finally:
        db.close()

