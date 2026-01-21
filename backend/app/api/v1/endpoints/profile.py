from fastapi import APIRouter, HTTPException, status
from typing import Dict, Any
import logging
from pydantic import BaseModel

class ProfileResponse(BaseModel):
    id: int
    name: str
    email: str
    title: str
    location: str
    about: str
    github_url: str
    linkedin_url: str
    portfolio_url: str
    created_at: str
    updated_at: str

class ErrorResponse(BaseModel):
    detail: str

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get(
    "/", 
    response_model=ProfileResponse,
    responses={
        200: {"description": "Profile retrieved successfully"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
async def get_profile() -> Dict[str, Any]:
    """
    Get the current user's profile information.
    
    Returns the complete profile information including personal details and social links.
    """
    try:
        return {
            "id": 1,
            "name": "Ishu Raj",
            "email": "ishuraj176@gmail.com",
            "title": "Full Stack Developer",
            "location": "India",
            "about": "Passionate developer building amazing things with code.",
            "github_url": "https://github.com/IshuRaj441",
            "linkedin_url": "https://www.linkedin.com/in/ishu-raj-13b840291/",
            "portfolio_url": "https://api-jd-ishuraj441.vercel.app/",
            "created_at": "2024-01-21T00:00:00",
            "updated_at": "2024-01-21T00:00:00"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving the profile: {str(e)}"
        )
