from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.db.models.profile import Profile
from app.schemas.profile import ProfileCreate, ProfileUpdate

def get_profile(db: Session, profile_id: int) -> Optional[Profile]:
    """Get a profile by ID."""
    return db.query(Profile).filter(Profile.id == profile_id).first()

def get_profile_by_email(db: Session, email: str) -> Optional[Profile]:
    """Get a profile by email (case-insensitive)."""
    return db.query(Profile).filter(Profile.email.ilike(email)).first()

def get_profiles(
    db: Session, *, skip: int = 0, limit: int = 100
) -> list[Profile]:
    """Get multiple profiles with pagination."""
    return db.query(Profile).offset(skip).limit(limit).all()

def create_profile(db: Session, *, obj_in: ProfileCreate) -> Profile:
    """Create a new profile."""
    db_obj = Profile(
        **obj_in.model_dump(exclude_unset=True),
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update_profile(
    db: Session, *, db_obj: Profile, obj_in: ProfileUpdate
) -> Profile:
    """Update a profile."""
    obj_data = jsonable_encoder(db_obj)
    update_data = obj_in.model_dump(exclude_unset=True)
    
    for field in obj_data:
        if field in update_data:
            setattr(db_obj, field, update_data[field])
    
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_profile(db: Session, *, profile_id: int) -> Profile:
    """Delete a profile."""
    obj = db.query(Profile).get(profile_id)
    if obj:
        db.delete(obj)
        db.commit()
    return obj
