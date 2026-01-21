from sqlalchemy import Column, Integer, String, DateTime, Text, Index, JSON
from sqlalchemy.sql import func
from typing import Dict, Any, Optional

from app.db.base_class import Base

class Profile(Base):
    """
    Database model representing a user's profile.
    
    This model stores personal and professional information about a user,
    including contact details, social media links, and profile metadata.
    """
    __tablename__ = "profiles"
    __table_args__ = (
        # Add a composite index for common query patterns
        Index('idx_profile_email_lower', func.lower('email'), unique=True),
        {
            'comment': 'Stores user profile information',
            'postgresql_partition_by': 'HASH (id)'  # Optional: For very large tables
        }
    )
    
    id = Column(
        Integer, 
        primary_key=True, 
        index=True,
        comment="Primary key and unique identifier for the profile"
    )
    
    name = Column(
        String(100), 
        nullable=False,
        index=True,
        comment="Full name of the user"
    )
    
    email = Column(
        String(255), 
        unique=True, 
        nullable=False, 
        index=True,
        comment="User's email address (must be unique)"
    )
    
    title = Column(
        String(200), 
        nullable=True,
        comment="Professional title or headline"
    )
    
    location = Column(
        String(200),
        nullable=True,
        index=True,
        comment="User's current location"
    )
    
    about = Column(
        Text,
        nullable=True,
        comment="Detailed bio or about information in markdown format"
    )
    
    github_url = Column(
        String(500),
        nullable=True,
        comment="URL to the user's GitHub profile"
    )
    
    linkedin_url = Column(
        String(500),
        nullable=True,
        comment="URL to the user's LinkedIn profile"
    )
    
    twitter_url = Column(
        String(500),
        nullable=True,
        comment="URL to the user's Twitter/X profile"
    )
    
    profile_picture_url = Column(
        String(500),
        nullable=True,
        comment="URL to the user's profile picture"
    )
    
    profile_metadata = Column(
        JSON,
        nullable=True,
        server_default='{}',
        comment="Additional metadata in JSON format"
    )
    
    created_at = Column(
        DateTime(timezone=True), 
        server_default=func.now(),
        nullable=False,
        comment="Timestamp when the profile was created"
    )
    
    updated_at = Column(
        DateTime(timezone=True), 
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        comment="Timestamp when the profile was last updated"
    )

    def __repr__(self) -> str:
        """String representation of the Profile instance."""
        return f"<Profile(id={self.id}, name='{self.name}', email='{self.email}')>"

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the Profile instance to a dictionary.
        
        Returns:
            Dict containing the profile data with ISO-formatted datetimes
        """
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "title": self.title,
            "location": self.location,
            "about": self.about,
            "github_url": self.github_url,
            "linkedin_url": self.linkedin_url,
            "twitter_url": self.twitter_url,
            "profile_picture_url": self.profile_picture_url,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "profile_metadata": self.profile_metadata or {},
            # For backward compatibility
            "metadata": self.profile_metadata or {}
        }
        
    def update_from_dict(self, data: Dict[str, Any]) -> None:
        """
        Update profile fields from a dictionary.
        
        Args:
            data: Dictionary containing the fields to update
        """
        for key, value in data.items():
            if hasattr(self, key) and not key.startswith('_'):
                setattr(self, key, value)
                
    @classmethod
    def get_required_fields(cls) -> list:
        """
        Get a list of required fields for the profile.
        
        Returns:
            List of required field names
        """
        return [
            'name', 
            'email'
        ]
