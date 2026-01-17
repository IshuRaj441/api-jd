from sqlalchemy.orm import Session
from app.db.database import engine, Base
from app.models.models import Profile, Skill, Project

# Create database tables
def init_db():
    Base.metadata.create_all(bind=engine)

def seed_db():
    from sqlalchemy.orm import sessionmaker
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Check if database is already seeded
        if db.query(Profile).first() is not None:
            print("Database already seeded")
            return
            
        # Create skills
        python = Skill(name="Python")
        fastapi = Skill(name="FastAPI")
        sqlalchemy = Skill(name="SQLAlchemy")
        javascript = Skill(name="JavaScript")
        react = Skill(name="React")
        
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
        
        # Create profile
        profile = Profile(
            name="Ishu Raj",
            email="ishu@email.com",
            education="B.Tech in Computer Science and Engineering"
        )
        
        # Add all to session and commit
        db.add_all([python, fastapi, sqlalchemy, javascript, react, project1, project2, profile])
        db.commit()
        print("Database seeded successfully")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

# Initialize the database
if __name__ == "__main__":
    init_db()
    seed_db()