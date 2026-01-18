from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from .project import Project

class ProfileBase(BaseModel):
    name: str
    email: EmailStr
    education: str

class ProfileCreate(ProfileBase):
    pass

class ProfileUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    education: Optional[str] = None

class Profile(ProfileBase):
    id: int
    projects: List[Project] = []
    
    class Config:
        orm_mode = True
        json_encoders = {
            'Profile': lambda p: {
                'id': p.id,
                'name': p.name,
                'email': p.email,
                'education': p.education,
                'projects': [
                    {
                        'id': proj.id,
                        'title': proj.title,
                        'description': proj.description,
                        'links': proj.links,
                        'skills': [{'id': s.id, 'name': s.name} for s in proj.skills]
                    } for proj in p.projects
                ]
            }
        }
