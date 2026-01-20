import logging
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from app.db.database import engine, Base, SessionLocal
from app.models.skill import Skill
from app.models.project import Project
from app.models.profile import Profile

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db():
    """Initialize the database by creating all tables."""
    try:
        # Import all models to ensure they are registered with SQLAlchemy
        from app import models  # noqa: F401
        
        logger.info("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
        
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise

def seed_initial_data():
    """Seed the database with initial data."""
    db = SessionLocal()
    
    try:
        logger.info("Checking if database needs seeding...")
        
        # Check if we already have data
        if db.query(Project).count() > 0 or db.query(Skill).count() > 0:
            logger.info("Database already contains data, skipping seeding")
            return
            
        logger.info("Seeding database with initial data...")
        
        # Create skills (all lowercase for consistency)
        python = Skill(name="python")
        fastapi = Skill(name="fastapi")
        sqlalchemy = Skill(name="sqlalchemy")
        javascript = Skill(name="javascript")
        react = Skill(name="react")
        ml = Skill(name="machine learning")
        docker = Skill(name="docker")
        rag = Skill(name="rag")
        streamlit = Skill(name="streamlit")
        
        # Create profile
        profile = Profile(
            name="Ishu Raj",
            email="ishuraj176@gmail.com",
            education="Bachelor's in Computer Science",
            headline="Full Stack Developer",
            location="India",
            bio="Passionate developer building amazing things with code.",
            links={
                'github': 'https://github.com/IshuRaj441',
                'linkedin': '',
                'portfolio': '',
                'twitter': ''
            }
        )
        
        # Create projects
        project1 = Project(
            title="Me-API Playground",
            description="Backend assessment project for showcasing skills and projects",
            links="https://github.com/ishuraj/me-api",
            profile=profile
        )
        project1.skills = [python, fastapi, sqlalchemy]
        
        project2 = Project(
            title="E-commerce Platform",
            description="Full-stack e-commerce platform with React and FastAPI",
            links="https://github.com/ishuraj/ecommerce",
            profile=profile
        )
        project2.skills = [python, javascript, react]
        
        # Add Python API Playground project
        python_project = Project(
            title="Python API Playground",
            description="A collection of Python projects and examples including FastAPI backends, data processing scripts, and API integrations. Demonstrates clean code, testing, and best practices.",
            links="https://github.com/IshuRaj441/api-jd",
            profile=profile
        )
        python_project.skills = [python, fastapi]
        
        # Create Python projects
        python_project1 = Project(
            title="Python API Project",
            description="A RESTful API built with FastAPI and SQLAlchemy",
            links="https://github.com/ishuraj/python-api-project"
        )
        python_project1.skills = [python, fastapi, sqlalchemy]
        
        python_project2 = Project(
            title="Machine Learning Model",
            description="A machine learning model for image classification",
            links="https://github.com/ishuraj/ml-project"
        )
        python_project2.skills = [python, ml]
        
        # Add a test project with python skill
        test_project = Project(
            title="Python Test Project",
            description="A test project to verify Python skill filtering",
            links="https://github.com/ishuraj/python-test",
            profile=profile
        )
        test_project.skills = [python]
        
        # Add all to session and commit
        db.add_all([
            python, fastapi, sqlalchemy, javascript, react, ml, docker, rag, streamlit,
            project1, project2, python_project, python_project1, python_project2, test_project
        ])
        db.commit()
        print("Database seeded successfully with projects and skills")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

def seed_db():
    """Wrapper function to initialize and seed the database."""
    init_db()
    seed_initial_data()

# Initialize the database
if __name__ == "__main__":
    seed_db()