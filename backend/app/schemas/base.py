from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BaseSchema(BaseModel):
    """Base schema that includes common configuration."""
    class Config:
        orm_mode = True

class BaseResponseSchema(BaseSchema):
    """Base response schema with common response fields."""
    id: int
    created_at: datetime
    updated_at: datetime

class ListResponseSchema(BaseSchema):
    """Base schema for list responses with pagination support."""
    total: int
    page: int
    size: int
    items: list[BaseResponseSchema]
