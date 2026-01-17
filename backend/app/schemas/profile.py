from pydantic import BaseModel, EmailStr
from typing import Optional

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
    
    class Config:
        orm_mode = True
