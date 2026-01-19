from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any
from datetime import datetime

from app.db.session import get_db
from app.schemas.profile import ProfileResponse
from app.repositories.profile import profile_repo

router = APIRouter()

@router.get("/", response_model=ProfileResponse)
async def get_profile(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    Get the user's profile information.
    """
    try:
        # In a real app, you would get the current user's ID from the auth token
        # For now, we'll get the first profile or create a default one
        profile = profile_repo.get_multi(db, limit=1)
        
        if not profile:
            # Create a default profile if none exists
            default_profile = {
                "name": "Ishu Raj",
                "email": "ishuraj176@gmail.com",
                "title": "Full Stack Developer",
                "location": "India",
                "about": "Passionate developer building amazing things with code.",
                "github_url": "https://github.com/IshuRaj441",
                "linkedin_url": "https://linkedin.com/in/ishuraj176",
                "twitter_url": "https://twitter.com/ishuraj176",
                "profile_picture_url": "https://github.com/IshuRaj441.png"
            }
            profile = profile_repo.create(db, obj_in=default_profile)
        else:
            profile = profile[0]
            
        return {
            "name": profile.name,
            "email": profile.email,
            "title": profile.title,
            "location": profile.location,
            "about": profile.about,
            "github_url": profile.github_url,
            "linkedin_url": profile.linkedin_url,
            "twitter_url": profile.twitter_url,
            "profile_picture_url": profile.profile_picture_url,
            "created_at": profile.created_at.isoformat() if profile.created_at else None,
            "updated_at": profile.updated_at.isoformat() if profile.updated_at else None
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while fetching profile: {str(e)}"
        )
