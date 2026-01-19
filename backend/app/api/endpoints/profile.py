from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime

router = APIRouter(prefix="/profile", tags=["profile"])

class ProfileResponse(BaseModel):
    name: str = Field(..., example="Ishu Raj")
    email: str = Field(..., example="ishuraj176@gmail.com")
    title: str = Field(..., example="Full Stack Developer")
    location: str = Field(..., example="India")
    about: str = Field(..., example="Passionate developer building amazing things with code.")
    github_url: str = Field(..., example="https://github.com/IshuRaj441")
    linkedin_url: str = Field(..., example="https://linkedin.com/in/ishuraj176")
    twitter_url: Optional[str] = Field(None, example="https://twitter.com/ishuraj176")
    profile_picture_url: str = Field(..., example="https://github.com/IshuRaj441.png")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# Static profile data
PROFILE_DATA = {
    "name": "Ishu Raj",
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

@router.get("/", response_model=ProfileResponse)
async def get_profile() -> ProfileResponse:
    """
    Returns the static profile data.
    This endpoint provides consistent profile information across restarts.
    """
    try:
        # Convert the static data to a Pydantic model for validation
        profile = ProfileResponse(
            name=PROFILE_DATA.get("name", ""),
            email=PROFILE_DATA.get("email", ""),
            title=PROFILE_DATA.get("title", ""),
            location=PROFILE_DATA.get("location", ""),
            about=PROFILE_DATA.get("about", ""),
            github_url=PROFILE_DATA.get("github_url", ""),
            linkedin_url=PROFILE_DATA.get("linkedin_url", ""),
            twitter_url=PROFILE_DATA.get("twitter_url"),
            profile_picture_url=PROFILE_DATA.get("profile_picture_url", ""),
        )
        return profile
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving profile: {str(e)}")

# Keep these endpoints for backward compatibility but make them no-ops
@router.post("/")
async def create_profile():
    """No-op endpoint for backward compatibility"""
    return {"message": "Profile is static and cannot be created"}

@router.put("/")
async def update_profile():
    """No-op endpoint for backward compatibility"""
    return {"message": "Profile is static and cannot be updated"}
