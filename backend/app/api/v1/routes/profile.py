from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.crud.profile import (
    get_profile, get_profile_by_email, get_profiles,
    create_profile, update_profile, delete_profile
)
from app.schemas.profile import Profile, ProfileCreate, ProfileUpdate

router = APIRouter()

@router.get("/", response_model=Profile, summary="Get my profile")
def read_profile(db: Session = Depends(get_db)):
    """
    Get the current user's profile.
    
    Returns the profile information of the currently authenticated user.
    """
    # In a real app, you would get the current user's ID from the auth token
    # For now, we'll just return the first profile or create a default one
    profile = get_profiles(db, skip=0, limit=1)
    if not profile:
        # Create a default profile if none exists
        profile_in = ProfileCreate(
            name="Ishu Raj",
            email="ishuraj441@gmail.com",
            title="Full Stack Developer",
            location="India",
            about="Passionate developer building amazing things with code.",
            github_url="https://github.com/IshuRaj441",
            linkedin_url="https://linkedin.com/in/ishuraj176",
            twitter_url="https://twitter.com/ishuraj176",
            profile_picture_url="https://github.com/IshuRaj441.png"
        )
        return create_profile(db=db, obj_in=profile_in)
    return profile[0]

@router.get("/all", response_model=List[Profile], summary="List all profiles")
def read_profiles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve all profiles with pagination.
    
    - **skip**: Number of profiles to skip (for pagination)
    - **limit**: Maximum number of profiles to return (max 100)
    """
    profiles = get_profiles(db, skip=skip, limit=min(limit, 100))
    return profiles

@router.get("/{profile_id}", response_model=Profile, summary="Get profile by ID")
def read_profile_by_id(profile_id: int, db: Session = Depends(get_db)):
    """
    Get a specific profile by its ID.
    
    - **profile_id**: The ID of the profile to retrieve
    """
    db_profile = get_profile(db, profile_id=profile_id)
    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return db_profile

@router.post("/", response_model=Profile, status_code=status.HTTP_201_CREATED, summary="Create a new profile")
def create_new_profile(profile: ProfileCreate, db: Session = Depends(get_db)):
    """
    Create a new user profile.
    
    - **name**: Full name of the user
    - **email**: Email address (must be unique)
    - **title**: Professional title (optional)
    - **location**: Current location (optional)
    - **about**: Brief bio (optional)
    - **github_url**: GitHub profile URL (optional)
    - **linkedin_url**: LinkedIn profile URL (optional)
    - **twitter_url**: Twitter profile URL (optional)
    - **profile_picture_url**: URL to profile picture (optional)
    """
    db_profile = get_profile_by_email(db, email=profile.email)
    if db_profile:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_profile(db=db, obj_in=profile)

@router.put("/{profile_id}", response_model=Profile, summary="Update a profile")
def update_existing_profile(
    profile_id: int, profile: ProfileUpdate, db: Session = Depends(get_db)
):
    """
    Update a profile's information.
    
    - **profile_id**: The ID of the profile to update
    - All other fields are optional and will only be updated if provided
    """
    db_profile = get_profile(db, profile_id=profile_id)
    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return update_profile(db=db, db_obj=db_profile, obj_in=profile)

@router.delete("/{profile_id}", response_model=Profile, summary="Delete a profile")
def delete_existing_profile(profile_id: int, db: Session = Depends(get_db)):
    """
    Delete a profile.
    
    - **profile_id**: The ID of the profile to delete
    """
    db_profile = delete_profile(db, profile_id=profile_id)
    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return db_profile
