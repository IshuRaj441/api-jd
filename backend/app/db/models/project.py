"""SQLAlchemy model for projects."""
from datetime import datetime
from typing import Any, Dict, List, Optional

from sqlalchemy import Boolean, DateTime, Integer, String, Text, func, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base

class Project(Base):
    """Project model for storing project information."""
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    skills: Mapped[List[str]] = mapped_column(JSON, nullable=False, server_default='[]')  # Storing as JSON array of strings
    github_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    demo_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    image_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    is_featured: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    status: Mapped[str] = mapped_column(String(20), default='active', nullable=False)
    project_metadata: Mapped[Optional[Dict[str, Any]]] = mapped_column('metadata', JSON, server_default='{}', nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Project(title='{self.title}')>"

    def to_dict(self) -> Dict[str, Any]:
        """Convert model instance to dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "skills": self.skills,
            "github_url": self.github_url,
            "demo_url": self.demo_url,
            "image_url": self.image_url,
            "is_featured": self.is_featured,
            "metadata": self.project_metadata,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
