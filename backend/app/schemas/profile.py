from pydantic import BaseModel, EmailStr, HttpUrl, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from .project import Project

class ProfileBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Full name of the user")
    email: EmailStr = Field(..., description="Email address of the user")
    title: str = Field(..., min_length=1, max_length=200, description="Professional title or headline")
    location: str = Field(..., min_length=1, max_length=200, description="Current location")
    about: str = Field(..., min_length=1, description="Detailed about/bio information")
    github_url: Optional[HttpUrl] = Field(None, description="GitHub profile URL")
    linkedin_url: Optional[HttpUrl] = Field(None, description="LinkedIn profile URL")
    twitter_url: Optional[HttpUrl] = Field(None, description="Twitter profile URL")
    profile_picture_url: Optional[HttpUrl] = Field(None, description="URL to profile picture")

class ProfileCreate(ProfileBase):
    pass

class ProfileUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="Full name of the user")
    email: Optional[EmailStr] = Field(None, description="Email address of the user")
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="Professional title or headline")
    location: Optional[str] = Field(None, min_length=1, max_length=200, description="Current location")
    about: Optional[str] = Field(None, min_length=1, description="Detailed about/bio information")
    github_url: Optional[HttpUrl] = Field(None, description="GitHub profile URL")
    linkedin_url: Optional[HttpUrl] = Field(None, description="LinkedIn profile URL")
    twitter_url: Optional[HttpUrl] = Field(None, description="Twitter profile URL")
    profile_picture_url: Optional[HttpUrl] = Field(None, description="URL to profile picture")

class ProfileInDBBase(ProfileBase):
    id: int = Field(..., description="Unique identifier for the profile")
    created_at: datetime = Field(..., description="Timestamp when the profile was created")
    updated_at: datetime = Field(..., description="Timestamp when the profile was last updated")

    class Config:
        orm_mode = True
        json_encoders = {
            'datetime': lambda dt: dt.isoformat() if dt else None
        }

class Profile(ProfileInDBBase):
    projects: List[Project] = Field(default_factory=list, description="List of projects associated with the profile")
    
    class Config:
        json_encoders = {
            'Profile': lambda p: {
                'id': p.id,
                'name': p.name,
                'email': p.email,
                'title': p.title,
                'location': p.location,
                'about': p.about,
                'github_url': str(p.github_url) if p.github_url else None,
                'linkedin_url': str(p.linkedin_url) if p.linkedin_url else None,
                'twitter_url': str(p.twitter_url) if p.twitter_url else None,
                'profile_picture_url': str(p.profile_picture_url) if p.profile_picture_url else None,
                'created_at': p.created_at.isoformat() if p.created_at else None,
                'updated_at': p.updated_at.isoformat() if p.updated_at else None,
                'projects': [
                    {
                        'id': proj.id,
                        'title': proj.title,
                        'description': proj.description,
                        'links': proj.links,
                        'skills': [{'id': s.id, 'name': s.name} for s in proj.skills]
                    } for proj in p.projects
                ] if hasattr(p, 'projects') else []
            }
        }

class ProfileResponse(BaseModel):
    success: bool = Field(True, description="Indicates if the request was successful")
    message: str = Field(..., description="Response message")
    data: Optional[Profile] = Field(None, description="Profile data if successful")

class ErrorResponse(BaseModel):
    success: bool = Field(False, description="Indicates if the request was successful")
    error: str = Field(..., description="Error message")
    error_code: Optional[str] = Field(None, description="Error code for programmatic handling")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")
