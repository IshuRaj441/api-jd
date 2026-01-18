from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from pathlib import Path

# Ensure the directory for the database exists
db_path = Path("app.db")
db_path.parent.mkdir(parents=True, exist_ok=True)

SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    # Import all models here to ensure they are registered with SQLAlchemy
    from app import models  # This will import all your models
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # You can add any initial data here if needed
    # db = SessionLocal()
    # try:
    #     # Add initial data here if needed
    #     db.commit()
    # finally:
    #     db.close()
