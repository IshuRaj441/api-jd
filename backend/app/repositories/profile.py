from typing import List, Optional
from sqlalchemy.orm import Session
from app.db.models.profile import Profile
from app.schemas.profile import ProfileCreate, ProfileUpdate
from .base import BaseRepository

class ProfileRepository(BaseRepository[Profile, ProfileCreate, ProfileUpdate]):
    def get_by_email(self, db: Session, email: str) -> Optional[Profile]:
        return db.query(self.model).filter(Profile.email == email).first()
    
    def get_multi_by_name(
        self, db: Session, *, name: str, skip: int = 0, limit: int = 100
    ) -> List[Profile]:
        return (
            db.query(self.model)
            .filter(Profile.name.ilike(f"%{name}%"))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_or_create(
        self, db: Session, *, obj_in: ProfileCreate
    ) -> Profile:
        db_obj = self.get_by_email(db, email=obj_in.email)
        if db_obj:
            return db_obj
        return self.create(db, obj_in=obj_in)

# Create a singleton instance
profile_repo = ProfileRepository(Profile)
