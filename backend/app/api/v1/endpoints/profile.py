from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any, List, Optional
from datetime import datetime
import logging

from app.db.session import get_db
from app.schemas.profile import (
    ProfileResponse, 
    ProfileCreate, 
    ProfileUpdate,
    ErrorResponse
)
from app.repositories.profile import profile_repo
from app.core.errors import APIError

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get(
    "/", 
    response_model=ProfileResponse,
    responses={
        200: {"description": "Profile retrieved successfully"},
        404: {"model": ErrorResponse, "description": "Profile not found"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
async def get_profile(
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get the current user's profile information.
    
    Returns the complete profile information including personal details and social links.
    In a real application, this would be protected and return the authenticated user's profile.
    """
    try:
        # In a real app, you would get the current user's ID from the auth token
        # For now, we'll get the first profile or create a default one
        profiles = profile_repo.get_multi(db, limit=1)
        
        if not profiles:
            # Create a default profile if none exists
            default_profile = ProfileCreate(
                name="Ishu Raj",
                email="ishuraj176@gmail.com",
                title="Full Stack Developer",
                location="India",
                about="Passionate developer building amazing things with code.",
                github_url="https://github.com/IshuRaj441",
                linkedin_url="https://linkedin.com/in/ishuraj176",
                twitter_url="https://twitter.com/ishuraj176",
                profile_picture_url="https://github.com/IshuRaj441.png"
            )
            profile, created = profile_repo.get_or_create(db, obj_in=default_profile)
        else:
            profile = profiles[0]
        
        return {
            "success": True,
            "message": "Profile retrieved successfully",
            "data": profile
        }
    except HTTPException as he:
        # Re-raise HTTP exceptions as they are
        raise he
    except Exception as e:
        logger.error(f"Unexpected error in get_profile: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while retrieving the profile"
        )

@router.put(
    "/", 
    response_model=ProfileResponse,
    responses={
        200: {"description": "Profile updated successfully"},
        400: {"model": ErrorResponse, "description": "Invalid input data"},
        404: {"model": ErrorResponse, "description": "Profile not found"},
        422: {"model": ErrorResponse, "description": "Validation error"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
async def update_profile(
    profile_update: ProfileUpdate,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Update the current user's profile information.
    
    Only the fields provided in the request will be updated.
    In a real application, this would be protected and update the authenticated user's profile.
    """
    try:
        # In a real app, get the current user's ID from the auth token
        profiles = profile_repo.get_multi(db, limit=1)
        if not profiles:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profile not found"
            )
            
        profile = profiles[0]
        updated_profile = profile_repo.update(
            db, 
            db_obj=profile, 
            obj_in=profile_update
        )
        
        return {
            "success": True,
            "message": "Profile updated successfully",
            "data": updated_profile
        }
            
    except HTTPException as he:
        # Re-raise HTTP exceptions as they are
        raise he
    except Exception as e:
        logger.error(f"Error updating profile: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while updating the profile"
        )

@router.get(
    "/all", 
    response_model=List[ProfileResponse],
    responses={
        200: {"description": "List of all profiles"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
async def list_profiles(
    skip: int = 0, 
    limit: int = 100,
    name: Optional[str] = None,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    List all profiles with optional filtering by name.
    
    This endpoint is typically protected and restricted to admin users in production.
    """
    try:
        if name:
            profiles = profile_repo.get_multi_by_name(
                db, 
                name=name, 
                skip=skip, 
                limit=limit
            )
        else:
            profiles = profile_repo.get_multi(
                db, 
                skip=skip, 
                limit=limit
            )
        
        return [
            {
                "success": True,
                "message": "Profiles retrieved successfully",
                "data": profile
            }
            for profile in profiles
        ]
    except Exception as e:
        logger.error(f"Error listing profiles: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving profiles"
        )
