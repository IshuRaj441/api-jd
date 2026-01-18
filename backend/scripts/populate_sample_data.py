import sys
import os
from datetime import datetime

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from app.db.database import Base, engine
from app.models.project import Project, ProjectSkill
from app.models.skill import Skill

def create_sample_skills(db: Session):
    """Create sample skills in the database."""
    skills = [
        {"name": "Python", "description": "Python programming language"},
        {"name": "FastAPI", "description": "Modern, fast web framework for building APIs"},
        {"name": "React", "description": "JavaScript library for building user interfaces"},
        {"name": "SQLAlchemy", "description": "SQL toolkit and ORM for Python"},
        {"name": "Docker", "description": "Containerization platform"},
        {"name": "JavaScript", "description": "JavaScript programming language"},
        {"name": "TypeScript", "description": "Typed superset of JavaScript"},
        {"name": "HTML/CSS", "description": "Web development fundamentals"},
        {"name": "Git", "description": "Version control system"},
        {"name": "RESTful APIs", "description": "Designing and building RESTful web services"},
    ]
    
    for skill_data in skills:
        # Check if skill already exists
        existing_skill = db.query(Skill).filter(Skill.name == skill_data["name"]).first()
        if not existing_skill:
            skill = Skill(**skill_data)
            db.add(skill)
    
    db.commit()
    print("✅ Sample skills created successfully!")

def create_sample_projects(db: Session):
    """Create sample projects and associate them with skills."""
    # Get all skills to reference them by name
    skills = {skill.name: skill for skill in db.query(Skill).all()}
    
    projects = [
        {
            "title": "Personal Portfolio Website",
            "description": "A responsive portfolio website built with React and FastAPI.",
            "links": {
                "github": "https://github.com/IshuRaj441/portfolio",
                "demo": "https://ishuraj.dev"
            },
            "skills": ["React", "TypeScript", "FastAPI", "Python"],
            "proficiency_levels": {"React": "Advanced", "TypeScript": "Intermediate", "FastAPI": "Advanced", "Python": "Advanced"}
        },
        {
            "title": "E-commerce API",
            "description": "A RESTful API for an e-commerce platform built with FastAPI and SQLAlchemy.",
            "links": {
                "github": "https://github.com/IshuRaj441/ecommerce-api"
            },
            "skills": ["FastAPI", "Python", "SQLAlchemy", "Docker"],
            "proficiency_levels": {"FastAPI": "Advanced", "Python": "Advanced", "SQLAlchemy": "Intermediate", "Docker": "Intermediate"}
        },
        {
            "title": "Task Management App",
            "description": "A full-stack task management application with React frontend and FastAPI backend.",
            "links": {
                "github": "https://github.com/IshuRaj441/task-manager",
                "demo": "https://tasks.ishuraj.dev"
            },
            "skills": ["React", "TypeScript", "FastAPI", "Python", "Docker"],
            "proficiency_levels": {"React": "Advanced", "TypeScript": "Intermediate", "FastAPI": "Advanced", "Python": "Advanced", "Docker": "Intermediate"}
        },
        {
            "title": "Blog Platform",
            "description": "A blogging platform with markdown support and user authentication.",
            "links": {
                "github": "https://github.com/IshuRaj441/blog-platform"
            },
            "skills": ["Python", "FastAPI", "SQLAlchemy", "JavaScript", "HTML/CSS"],
            "proficiency_levels": {"Python": "Advanced", "FastAPI": "Advanced", "SQLAlchemy": "Intermediate", "JavaScript": "Intermediate", "HTML/CSS": "Intermediate"}
        },
        {
            "title": "Weather Dashboard",
            "description": "A real-time weather dashboard showing forecasts from multiple providers.",
            "links": {
                "github": "https://github.com/IshuRaj441/weather-dashboard",
                "demo": "https://weather.ishuraj.dev"
            },
            "skills": ["React", "TypeScript", "RESTful APIs"],
            "proficiency_levels": {"React": "Advanced", "TypeScript": "Intermediate", "RESTful APIs": "Advanced"}
        }
    ]
    
    for project_data in projects:
        # Check if project already exists
        existing_project = db.query(Project).filter(Project.title == project_data["title"]).first()
        if not existing_project:
            # Create the project
            project = Project(
                title=project_data["title"],
                description=project_data["description"],
                links=project_data["links"]
            )
            db.add(project)
            db.flush()  # Flush to get the project ID
            
            # Add skill associations
            for skill_name in project_data["skills"]:
                skill = skills.get(skill_name)
                if skill:
                    project_skill = ProjectSkill(
                        project_id=project.id,
                        skill_id=skill.id,
                        proficiency_level=project_data["proficiency_levels"].get(skill_name, "Intermediate")
                    )
                    db.add(project_skill)
            
            db.commit()
    
    print("✅ Sample projects created successfully!")

def main():
    print("🚀 Starting to populate database with sample data...")
    
    # Create all tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    # Create a new database session
    db = Session(autocommit=False, autoflush=False, bind=engine)
    
    try:
        create_sample_skills(db)
        create_sample_projects(db)
        print("✨ Database populated successfully!")
    except Exception as e:
        print(f"❌ Error populating database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()
