from typing import List, Optional
from sqlalchemy.orm import Session
from app.db.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate
from .base import BaseRepository

class ProjectRepository(BaseRepository[Project, ProjectCreate, ProjectUpdate]):
    def get_multi_by_skill(
        self, db: Session, *, skill: str, skip: int = 0, limit: int = 100
    ) -> List[Project]:
        """
        Get projects filtered by skill.
        """
        return (
            db.query(self.model)
            .filter(Project.skills.any(skill.lower()))
            .offset(skip)
            .limit(limit)
            .all()
        )

# Create a singleton instance
project_repo = ProjectRepository(Project)
