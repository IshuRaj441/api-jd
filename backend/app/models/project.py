from sqlalchemy import Column, String, Text, ForeignKey, Table, JSON
from sqlalchemy.orm import relationship
from .base import BaseModel
from ..core.database import Base

# Association table for many-to-many relationship between Project and Skill
project_skill_association = Table(
    'project_skills',
    Base.metadata,
    Column('project_id', ForeignKey('project.id'), primary_key=True),
    Column('skill_id', ForeignKey('skills.id'), primary_key=True)
)

class ProjectSkill(BaseModel):
    __tablename__ = 'project_skills_meta'
    
    project_id = Column(ForeignKey('project.id'), primary_key=True)
    skill_id = Column(ForeignKey('skills.id'), primary_key=True)
    proficiency_level = Column(String(50), nullable=True)  # e.g., 'Beginner', 'Intermediate', 'Advanced'
    
    # Relationships
    project = relationship("Project", back_populates="skills_meta")
    skill = relationship("Skill", back_populates="projects")

class Project(BaseModel):
    __tablename__ = 'project'
    
    title = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=False)
    links = Column(JSON, default=dict)  # Store GitHub, demo links, etc.
    
    # Relationships
    skills_meta = relationship("ProjectSkill", back_populates="project")
    
    @property
    def skills(self):
        return [ps.skill for ps in self.skills_meta]
    
    def __repr__(self):
        return f"<Project(id={self.id}, title='{self.title}')>"
