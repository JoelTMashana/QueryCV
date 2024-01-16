from sqlalchemy.orm import Session
from models import Experience, Skill, Tool, User, UserSkillLink, UserToolLink, ExperienceSkillLink, ExperienceToolLink
import logging


# def initialise_db(engine):
#     """
#     Initilaises the database with predefined data if the db is empty.
#     """
#     db = Session(bind=engine)
#     print('Initialise DB called')
#     try:
#         if db.query(Experience).count() == 0:
#             initial_experiences = [
#                 Experience(position="Junior Full Stack Developer",
#                         company="Crossflow Payments",
#                         industry="Financial Technology",
#                         duration="13/06/2023 - 11/12/2023",
#                         skills="Collaboration, Communication, Organisation",
#                         experience="Played a pivotal role in the migration from Angular to React/Next.js, employing an Agile methodology. This was achieved through daily standups and strategic sprint planning while adhering to the MVC design pattern and applying DRY and SOLID principles",
#                         tools="React , Next.js, TypeScript, JavaScript, GitLab,  VS Code",
#                         outcomes="Successful delivery of the migration project, leading to 30/%/ speed increase and improved user experience"),
#                 Experience(position="Junior Full Stack Developer",
#                         company="Crossflow Payments",
#                         industry="Financial Technology",
#                         duration="13/06/2023 - 11/12/2023",
#                         skills="Problem Solving, Creativity, Prototyping",
#                         experience="Independently revamped the Angular navigation bar to a more user-friendly, responsive design by integrating modern UI/UX principles.",
#                         tools="React , Next.js, TypeScript, JavaScript, GitLab,  VS Code",
#                         outcomes="Resulted in navigation menu supporting potential new features and better user engagement"),
#                 Experience(position="Junior Full Stack Developer",
#                         company="Star Editions",
#                         industry="E-commerce",
#                         duration="06/08/2021 - 11/02/2022",
#                         skills="Team Work, Collaboration,  Stakeholder engagement, Customer focus, Product focus, Requirements gathering",
#                         experience="Captured client requirements, then designed and developed bespoke websites in collaboration with the development team.",
#                         tools="Javascript, Shopify, Adobe suite, Jquery, CSS, Liquid",
#                         outcomes="Successful delivery of projects in a timely and efficient manner. Product and client focused delivery satisfying customer needs."),
#                 Experience(position="Junior Full Stack Developer",
#                         company="Crossflow Payments",
#                         industry="Financial Technology",
#                         duration="13/06/2023 - 11/12/2023",
#                         skills="Communication, Problem Solving",
#                         experience="Developed a backend feature that automates notifications to corporates and SMEs upon invoice reconciliation. ",
#                         tools="PHP, Laravel, MySQL, REST API, GitLab",
#                         outcomes="Resulting in a 50% reduction in admin hours spent monitoring the status of invoices and increased system transparency."),
#                 Experience(position="Junior Full Stack Developer",
#                         company="Crossflow Payments",
#                         industry="Financial Technology",
#                         duration="13/06/2023 - 11/12/2023",
#                         skills="Initiative, Research and Development, Experimentation, Testing",
#                         experience="Led the design of the React frontend using Figma. Styled components using Tailwind CSS.",
#                         tools="Tailwind CSS, Figma",
#                         outcomes="Resulting in a clear road map for execution, while ensuring responsive web design."),
#                 Experience(position="Junior Full Stack Developer",
#                         company="Crossflow Payments",
#                         industry="Financial Technology",
#                         duration="13/06/2023 - 11/12/2023",
#                         skills="Team Work, Collaboration, Code Reviews",
#                         experience="Leveraged GitLab for version control and continuous integration/continuous deployment across 3 applications, facilitating code integration, automated testing, and efficient deployment processes",
#                         tools="Gitlab, CI/CD",
#                         outcomes="Played a crucial role in maintaining code quality. Producing scalable and maintainable code."),
#                 Experience(position="Junior Full Stack Developer",
#                         company="Crossflow Payments",
#                         industry="Financial Technology",
#                         duration="13/06/2023 - 11/12/2023",
#                         skills="Research, Written Communication, Oral Presentation",
#                         experience="Retrieved hyperparameters of an inaccessible Neural Network and composed a report evaluating the Machine Learning system. I effectively communicated findings to senior non-technical stakeholders",
#                         tools="Gitlab, Machine Learning, Artificial Neural Networks, K-means, PCA",
#                         outcomes="Provided insights that informed future strategic directions. Discerned state of the system. Retrieved deleted Neural Network."),
#                 Experience(position="Junior Full Stack Developer",
#                         company="Crossflow Payments",
#                         industry="Financial Technology",
#                         duration="13/06/2023 - 11/12/2023",
#                         skills="Autonomous, Independent working",
#                         experience="Independently managed local development environments, including repository retrieval, configuring VS Code extensions, utilising Docker for containerised setups, importing databases from AWS to HeidiSQL and accessing the VPN-protected API",
#                         tools="Docker, Gitlab, MySQL, HeidiSQL, VS Code, AWS",
#                         outcomes="Allowed me to work indepedently, ensuring that I am capable of working with the system on my own."),
#             ]

#             db.add_all(initial_experiences)  
#             db.commit() 
#             logging.info("Database initialised with predefined experiences.")
#         else:
#             logging.info("Database already contains experiences.")
#     except Exception as e:
#         logging.error(f"Error initialising database: {e}")
#     finally:
#         db.close()

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

