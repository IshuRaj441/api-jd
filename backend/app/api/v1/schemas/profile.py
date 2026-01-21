from pydantic import BaseModel, EmailStr, HttpUrl, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class ProfileBase(BaseModel):
    name: str = Field(..., max_length=100, description="Full name of the user")
    email: EmailStr = Field(..., description="User's email address")
    title: Optional[str] = Field(None, max_length=200, description="Professional title or headline")
    location: Optional[str] = Field(None, max_length=100, description="Current location")
    about: Optional[str] = Field(None, description="Brief bio or about section")
    github_url: Optional[HttpUrl] = Field(None, description="GitHub profile URL")
    linkedin_url: Optional[HttpUrl] = Field(None, description="LinkedIn profile URL")
    twitter_url: Optional[HttpUrl] = Field(None, description="Twitter profile URL")
    profile_picture_url: Optional[HttpUrl] = Field(None, description="URL to profile picture")

class ProfileCreate(ProfileBase):
    pass

class ProfileUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100, description="Full name of the user")
    email: Optional[EmailStr] = Field(None, description="User's email address")
    title: Optional[str] = Field(None, max_length=200, description="Professional title or headline")
    location: Optional[str] = Field(None, max_length=100, description="Current location")
    about: Optional[str] = Field(None, description="Brief bio or about section")
    github_url: Optional[HttpUrl] = Field(None, description="GitHub profile URL")
    linkedin_url: Optional[HttpUrl] = Field(None, description="LinkedIn profile URL")
    twitter_url: Optional[HttpUrl] = Field(None, description="Twitter profile URL")
    profile_picture_url: Optional[HttpUrl] = Field(None, description="URL to profile picture")

class ProfileInDBBase(ProfileBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Profile(ProfileInDBBase):
    pass
