from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any
import logging

from app.db.session import get_db
from app.schemas.profile import ProfileResponse, ErrorResponse

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
async def get_profile(db: Session = Depends(get_db)) -> Dict[str, Any]:
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
            "linkedin_url": "https://linkedin.com/in/ishuraj176",
            "portfolio_url": "",
            "twitter_url": "https://twitter.com/ishuraj176",
            "created_at": "2024-01-21T00:00:00",
            "updated_at": "2024-01-21T00:00:00"
        }
    except Exception as e:
        logger.error(f"Error retrieving profile: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving the profile"
        )
