from typing import List, Optional, Dict, Any, Union, Tuple
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from fastapi import HTTPException, status
import logging

from app.db.models.profile import Profile
from app.schemas.profile import ProfileCreate, ProfileUpdate
from .base import BaseRepository

logger = logging.getLogger(__name__)

class ProfileRepository(BaseRepository[Profile, ProfileCreate, ProfileUpdate]):
    def get_by_email(self, db: Session, email: str) -> Optional[Profile]:
        """
        Retrieve a profile by email address.
        
        Args:
            db: Database session
            email: Email address to search for
            
        Returns:
            Optional[Profile]: The profile if found, None otherwise
            
        Raises:
            HTTPException: If there's an error accessing the database
        """
        try:
            return db.query(self.model).filter(Profile.email == email).first()
        except SQLAlchemyError as e:
            logger.error(f"Error fetching profile by email {email}: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error retrieving profile by email"
            )
    
    def get_multi(
        self, 
        db: Session, 
        *, 
        skip: int = 0, 
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Profile]:
        """
        Retrieve multiple profiles with optional filtering.
        
        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            filters: Dictionary of field-value pairs to filter by
            
        Returns:
            List[Profile]: List of profiles matching the criteria
            
        Raises:
            HTTPException: If there's an error accessing the database
        """
        try:
            query = db.query(self.model)
            
            # Apply filters if provided
            if filters:
                for field, value in filters.items():
                    if hasattr(self.model, field):
                        query = query.filter(getattr(self.model, field) == value)
            
            return query.offset(skip).limit(limit).all()
        except SQLAlchemyError as e:
            logger.error(f"Error fetching profiles: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error retrieving profiles"
            )
    
    def get_multi_by_name(
        self, 
        db: Session, 
        *, 
        name: str, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Profile]:
        """
        Search profiles by name using case-insensitive partial matching.
        
        Args:
            db: Database session
            name: Name or part of name to search for
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List[Profile]: List of matching profiles
            
        Raises:
            HTTPException: If there's an error accessing the database
        """
        try:
            return (
                db.query(self.model)
                .filter(Profile.name.ilike(f"%{name}%"))
                .offset(skip)
                .limit(limit)
                .all()
            )
        except SQLAlchemyError as e:
            logger.error(f"Error searching profiles by name '{name}': {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error searching profiles"
            )
    
    def create(self, db: Session, *, obj_in: ProfileCreate) -> Profile:
        """
        Create a new profile.
        
        Args:
            db: Database session
            obj_in: Profile data to create
            
        Returns:
            Profile: The created profile
            
        Raises:
            HTTPException: If there's an error creating the profile or a duplicate email
        """
        try:
            db_obj = self.model(**obj_in.dict(exclude_unset=True))
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except IntegrityError as e:
            db.rollback()
            logger.error(f"Integrity error creating profile: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Error creating profile: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error creating profile"
            )
    
    def update(
        self, 
        db: Session, 
        *, 
        db_obj: Profile, 
        obj_in: Union[ProfileUpdate, Dict[str, Any]]
    ) -> Profile:
        """
        Update a profile.
        
        Args:
            db: Database session
            db_obj: The profile to update
            obj_in: New profile data (can be a dictionary or Pydantic model)
            
        Returns:
            Profile: The updated profile
            
        Raises:
            HTTPException: If there's an error updating the profile
        """
        try:
            update_data = obj_in.dict(exclude_unset=True) if not isinstance(obj_in, dict) else obj_in
            
            for field, value in update_data.items():
                setattr(db_obj, field, value)
            
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except IntegrityError as e:
            db.rollback()
            logger.error(f"Integrity error updating profile {db_obj.id}: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already in use"
            )
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Error updating profile {db_obj.id}: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error updating profile"
            )
    
    def get_or_create(
        self, 
        db: Session, 
        *, 
        obj_in: ProfileCreate
    ) -> Tuple[Profile, bool]:
        """
        Get an existing profile by email or create a new one if it doesn't exist.
        
        Args:
            db: Database session
            obj_in: Profile data to create if not exists
            
        Returns:
            Tuple[Profile, bool]: The profile and a boolean indicating if it was created
            
        Raises:
            HTTPException: If there's an error accessing or creating the profile
        """
        try:
            db_obj = self.get_by_email(db, email=obj_in.email)
            if db_obj:
                return db_obj, False
                
            db_obj = self.create(db, obj_in=obj_in)
            return db_obj, True
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error in get_or_create for profile: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error in profile operation"
            )

# Create a singleton instance
profile_repo = ProfileRepository(Profile)
