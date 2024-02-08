from config import SQLALCHEMY_DATABASE_URL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging
from models import  Base
from initial_data import initialise_db

logging.basicConfig(level=logging.INFO)

# if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
#     engine = create_engine(
#         SQLALCHEMY_DATABASE_URL, 
#         connect_args={"check_same_thread": False}
#     )
# else:
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """
    Dependency function for FastAPI to provide a database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Base.metadata.create_all(bind=engine)

initialise_db(engine) 