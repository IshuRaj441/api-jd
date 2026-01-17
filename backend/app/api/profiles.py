from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any

from app import models, schemas
from app.api.deps import get_db, get_current_active_user
from app.core.config import settings

router = APIRouter()

@router.post("/profile", response_model=schemas.ProfileResponse, status_code=status.HTTP_201_CREATED)
def create_profile(
    profile_in: schemas.ProfileCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    """
    Create a new profile.
    """
    # Check if profile already exists for this user
    db_profile = db.query(models.Profile).filter(
        models.Profile.email == profile_in.email
    ).first()
    
    if db_profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Profile with this email already exists"
        )
    
    # Convert Pydantic model to dict and create SQLAlchemy model
    profile_data = profile_in.model_dump()
    profile_links = profile_data.pop('links', {})
    
    # Create profile
    db_profile = models.Profile(
        **profile_data,
        links=profile_links
    )
    
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    
    return db_profile

@router.get("/profile", response_model=schemas.ProfileResponse)
def read_profile(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    """
    Get the current user's profile.
    """
    # In a real app, we'd use current_user.id to fetch the profile
    db_profile = db.query(models.Profile).first()
    
    if db_profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    
    return db_profile

@router.put("/profile", response_model=schemas.ProfileResponse)
def update_profile(
    profile_in: schemas.ProfileUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    """
    Update the current user's profile.
    """
    # In a real app, we'd use current_user.id to fetch the profile
    db_profile = db.query(models.Profile).first()
    
    if db_profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    
    # Update profile data
    update_data = profile_in.model_dump(exclude_unset=True)
    
    # Handle links update
    if 'links' in update_data:
        links = {**db_profile.links, **update_data.pop('links')}
        update_data['links'] = links
    
    # Update fields
    for field, value in update_data.items():
        setattr(db_profile, field, value)
    
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    
    return db_profile

@router.get("/search", response_model=Dict[str, Any])
def search_profiles(
    q: str,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 10
):
    """
    Search profiles by name, email, or skills.
    """
    search = f"%{q}%"
    
    # Search in profiles
    profiles = db.query(models.Profile).filter(
        (models.Profile.name.ilike(search)) |
        (models.Profile.email.ilike(search)) |
        (models.Profile.headline.ilike(search) if models.Profile.headline else False)
    ).offset(skip).limit(limit).all()
    
    # Search in skills
    skills = db.query(models.Skill).filter(
        models.Skill.name.ilike(search)
    ).offset(skip).limit(limit).all()
    
    # Search in projects
    projects = db.query(models.Project).filter(
        (models.Project.title.ilike(search)) |
        (models.Project.description.ilike(search))
    ).offset(skip).limit(limit).all()
    
    return {
        "profiles": profiles,
        "skills": skills,
        "projects": projects
    }
