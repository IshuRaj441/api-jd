from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.models.models import Profile as DBProfile
from app.schemas import Profile, ProfileCreate, ProfileUpdate

router = APIRouter()

@router.get("/health")
async def health_check():
    return {"status": "ok"}

@router.post("/profile", response_model=Profile)
def create_profile(profile: ProfileCreate, db: Session = Depends(get_db)):
    db_profile = DBProfile(**profile.dict())
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

@router.get("/profile", response_model=Profile)
def read_profile(db: Session = Depends(get_db)):
    profile = db.query(DBProfile).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@router.put("/profile", response_model=Profile)
def update_profile(profile_update: ProfileUpdate, db: Session = Depends(get_db)):
    db_profile = db.query(DBProfile).first()
    if not db_profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    update_data = profile_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_profile, field, value)
    
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile
