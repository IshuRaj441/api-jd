from sqlalchemy.orm import Session
from app.db.database import engine, Base
from app.models.models import Skill, Project

# Create database tables
def init_db():
    # Only create tables for skills and projects
    Base.metadata.create_all(bind=engine, tables=[
        Skill.__table__,
        Project.__table__
    ])

def seed_db():
    from sqlalchemy.orm import sessionmaker
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Clear existing data to ensure clean seed
        db.query(Project).delete()
        db.query(Skill).delete()
        db.commit()
            
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
        
        # Create projects
        project1 = Project(
            title="Me-API Playground",
            description="Backend assessment project for showcasing skills and projects",
            links="https://github.com/ishuraj/me-api"
        )
        project1.skills = [python, fastapi, sqlalchemy]
        
        project2 = Project(
            title="E-commerce Platform",
            description="Full-stack e-commerce platform with React and FastAPI",
            links="https://github.com/ishuraj/ecommerce"
        )
        project2.skills = [python, javascript, react]
        
        # Add Python API Playground project
        python_project = Project(
            title="Python API Playground",
            description="A collection of Python projects and examples including FastAPI backends, data processing scripts, and API integrations. Demonstrates clean code, testing, and best practices.",
            links="https://github.com/IshuRaj441/api-jd"
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
        
        # Add all to session and commit
        db.add_all([
            python, fastapi, sqlalchemy, javascript, react, ml, docker, rag, streamlit,
            project1, project2, python_project, python_project1, python_project2
        ])
        db.commit()
        print("Database seeded successfully with projects and skills")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

# Initialize the database
if __name__ == "__main__":
    init_db()
    seed_db()