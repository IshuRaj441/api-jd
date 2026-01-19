"""
Script to populate the database with sample project data.

Run with: python -m scripts.populate_sample_projects
"""
import sys
from pathlib import Path
from typing import Any, Dict, List

# Add the project root to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db.models.project import Project
from app.schemas.project import ProjectCreate, ProjectStatus

# Sample project data
SAMPLE_PROJECTS: List[Dict[str, Any]] = [
    {
        "title": "Portfolio Website",
        "description": "A modern portfolio website built with React and FastAPI",
        "skills": ["python", "fastapi", "react", "typescript", "tailwindcss"],
        "github_url": "https://github.com/example/portfolio",
        "demo_url": "https://portfolio.example.com",
        "image_url": "https://via.placeholder.com/800x600?text=Portfolio+Website",
        "is_featured": True,
        "status": ProjectStatus.ACTIVE,
        "metadata": {
            "tech_stack": ["python", "fastapi", "react", "typescript", "tailwindcss"],
            "year": 2024
        }
    },
    {
        "title": "E-commerce Platform",
        "description": "A full-stack e-commerce platform with payment integration",
        "skills": ["python", "django", "postgresql", "react", "stripe"],
        "github_url": "https://github.com/example/ecommerce",
        "demo_url": "https://shop.example.com",
        "image_url": "https://via.placeholder.com/800x600?text=E-commerce+Platform",
        "is_featured": True,
        "status": ProjectStatus.ACTIVE,
        "metadata": {
            "tech_stack": ["python", "django", "postgresql", "react", "stripe"],
            "year": 2023
        }
    },
    {
        "title": "Task Management App",
        "description": "A collaborative task management application",
        "skills": ["javascript", "nodejs", "mongodb", "express", "react"],
        "github_url": "https://github.com/example/task-manager",
        "demo_url": "https://tasks.example.com",
        "image_url": "https://via.placeholder.com/800x600?text=Task+Manager",
        "is_featured": False,
        "status": ProjectStatus.ACTIVE,
        "metadata": {
            "tech_stack": ["javascript", "nodejs", "mongodb", "express", "react"],
            "year": 2023
        }
    }
]

def init_db(db: Session) -> None:
    """Initialize the database with sample projects."""
    # Check if projects already exist
    if db.query(Project).count() > 0:
        print("Database already has projects. Skipping sample data population.")
        return
    
    # Create sample projects
    for project_data in SAMPLE_PROJECTS:
        project = Project(**project_data)
        db.add(project)
    
    # Commit the changes
    db.commit()
    print(f"Added {len(SAMPLE_PROJECTS)} sample projects to the database.")

def main() -> None:
    """Main function to run the script."""
    db = SessionLocal()
    try:
        init_db(db)
    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()
