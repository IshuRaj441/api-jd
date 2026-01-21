from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class ProjectBase(BaseModel):
    title: str = Field(..., max_length=200, description="Title of the project")
    description: Optional[str] = Field(None, description="Detailed description of the project")
    skills: List[str] = Field(default_factory=list, description="List of skills/technologies used")
    github_url: Optional[HttpUrl] = Field(None, description="GitHub repository URL")
    demo_url: Optional[HttpUrl] = Field(None, description="Live demo URL")
    image_url: Optional[HttpUrl] = Field(None, description="URL to project image")
    is_featured: bool = Field(False, description="Whether the project is featured")
    status: str = Field("active", description="Project status (active, completed, archived)")
    project_metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=200, description="Title of the project")
    description: Optional[str] = Field(None, description="Detailed description of the project")
    skills: Optional[List[str]] = Field(None, description="List of skills/technologies used")
    github_url: Optional[HttpUrl] = Field(None, description="GitHub repository URL")
    demo_url: Optional[HttpUrl] = Field(None, description="Live demo URL")
    image_url: Optional[HttpUrl] = Field(None, description="URL to project image")
    is_featured: Optional[bool] = Field(None, description="Whether the project is featured")
    status: Optional[str] = Field(None, description="Project status (active, completed, archived)")
    project_metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")

class ProjectInDBBase(ProjectBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Project(ProjectInDBBase):
    pass
