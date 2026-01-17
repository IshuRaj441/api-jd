from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship
from .base import BaseModel

class Skill(BaseModel):
    __tablename__ = 'skills'
    
    name = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    
    # Relationships
    projects = relationship("ProjectSkill", back_populates="skill")
    
    def __repr__(self):
        return f"<Skill(id={self.id}, name='{self.name}')>"
