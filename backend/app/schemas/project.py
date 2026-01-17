from pydantic import BaseModel
from typing import List, Optional
from .skill import Skill

class ProjectBase(BaseModel):
    title: str
    description: str
    links: str

class ProjectCreate(ProjectBase):
    skill_ids: List[int] = []

class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    links: Optional[str] = None
    skill_ids: Optional[List[int]] = None

class Project(ProjectBase):
    id: int
    skills: List[Skill] = []
    
    class Config:
        orm_mode = True
