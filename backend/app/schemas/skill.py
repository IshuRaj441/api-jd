from typing import Optional, List
from pydantic import BaseModel, Field
from .base import BaseSchema, BaseResponseSchema

class SkillBase(BaseModel):
    """Base schema for Skill operations."""
    name: str

class SkillCreate(SkillBase):
    """Schema for creating a new skill."""
    pass

class Skill(SkillBase):
    """Schema for skill data."""
    id: int
    
    class Config:
        orm_mode = True

class SkillResponse(Skill):
    """Schema for skill response with related data."""
    project_count: int = Field(0, description="Number of projects using this skill")

class SkillListResponse(BaseSchema):
    """Schema for a paginated list of skills."""
    total: int
    items: List[SkillResponse]
