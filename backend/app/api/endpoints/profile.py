from fastapi import APIRouter
from typing import Dict, Any
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

class Profile(BaseModel):
    name: str = "Ishu raj"
    email: str = "ishuraj176@gmail.com"
    title: str = "Full Stack Developer"
    location: str = "India"
    about: str = "Passionate developer building amazing things with code."
    github_url: str = "https://github.com/IshuRaj441"
    linkedin_url: str = "https://linkedin.com/in/ishuraj176"
    twitter_url: str = "https://twitter.com/ishuraj176"
    profile_picture_url: str = "https://github.com/IshuRaj441.png"
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()

# Static profile data
PROFILE_DATA = {
    "name": "Ishu raj",
    "email": "ishuraj176@gmail.com",
    "education": "B.Tech (IT)",
    "title": "Full Stack Developer",
    "location": "India",
    "about": "Passionate developer building amazing things with code.",
    "github_url": "https://github.com/IshuRaj441",
    "linkedin_url": "https://linkedin.com/in/ishuraj176",
    "twitter_url": "https://twitter.com/ishuraj176",
    "profile_picture_url": "https://github.com/IshuRaj441.png",
    "created_at": "2024-01-19T00:00:00Z",
    "updated_at": "2024-01-19T00:00:00Z"
}

@router.get("/health")
async def health_check():
    return {"status": "ok"}

@router.get("/profile", response_model=Profile)
def read_profile():
    """
    Returns the static profile data.
    This endpoint doesn't hit the database, ensuring consistent data across restarts.
    """
    return PROFILE_DATA

# Keep these endpoints for backward compatibility but make them no-ops
@router.post("/profile", response_model=Profile)
def create_profile():
    """No-op endpoint for backward compatibility"""
    return PROFILE_DATA

@router.put("/profile", response_model=Profile)
def update_profile():
    """No-op endpoint for backward compatibility"""
    return PROFILE_DATA
