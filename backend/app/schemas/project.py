from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, HttpUrl, validator

class ProjectStatus(str, Enum):
    ACTIVE = "active"
    ARCHIVED = "archived"
    DRAFT = "draft"

class ProjectBase(BaseModel):
    """Base project schema with common fields."""
    title: str = Field(..., max_length=200, description="Title of the project")
    description: Optional[str] = Field(None, description="Detailed description of the project")
    skills: List[str] = Field(
        default_factory=list,
        description="List of skills/technologies used in the project"
    )
    github_url: Optional[HttpUrl] = Field(None, description="URL to the project's GitHub repository")
    demo_url: Optional[HttpUrl] = Field(None, description="URL to the live demo of the project")
    image_url: Optional[HttpUrl] = Field(None, description="URL to the project's cover image")
    is_featured: bool = Field(False, description="Whether the project is featured")
    status: ProjectStatus = Field(ProjectStatus.ACTIVE, description="Current status of the project")
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional metadata for the project"
    )

    @validator('skills', each_item=True)
    def validate_skill_length(cls, v):
        if len(v) > 50:
            raise ValueError('Skill must be less than 50 characters')
        return v.lower()

class ProjectCreate(ProjectBase):
    """Schema for creating a new project."""
    pass

class ProjectUpdate(BaseModel):
    """Schema for updating an existing project."""
    title: Optional[str] = Field(None, max_length=200, description="Updated title of the project")
    description: Optional[str] = Field(None, description="Updated description")
    skills: Optional[List[str]] = Field(None, description="Updated list of skills")
    github_url: Optional[HttpUrl] = Field(None, description="Updated GitHub URL")
    demo_url: Optional[HttpUrl] = Field(None, description="Updated demo URL")
    image_url: Optional[HttpUrl] = Field(None, description="Updated image URL")
    is_featured: Optional[bool] = Field(None, description="Whether to feature this project")
    status: Optional[ProjectStatus] = Field(None, description="Updated status of the project")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata updates")

class ProjectInDBBase(ProjectBase):
    """Base schema for project data coming from the database."""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class Project(ProjectInDBBase):
    """Complete project schema for API responses."""
    pass

class ProjectInDB(ProjectInDBBase):
    """Project schema for data stored in the database."""
    pass

class ProjectResponse(BaseModel):
    """Standard response format for project endpoints."""
    success: bool
    message: str
    data: Optional[Project] = None
