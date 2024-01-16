
import os

TESTING = os.environ.get("TESTING")

if TESTING:
    SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
else:
    SQLALCHEMY_DATABASE_URL = "sqlite:///./user_work_experience.db"



