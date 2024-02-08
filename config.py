import os

TESTING = os.environ.get("TESTING")

if TESTING:
    SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
else:
    SQLALCHEMY_DATABASE_URL = os.environ.get("DATABASE_URL").replace("postgres://", "postgresql://", 1) if os.environ.get("DATABASE_URL") else f"postgresql://postgres:Takudzwanashe8!@localhost:5432/user_work_experience"
