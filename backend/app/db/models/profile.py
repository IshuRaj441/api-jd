from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from app.db.base_class import Base

class Profile(Base):
    __tablename__ = "profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    title = Column(String(100), nullable=False)
    location = Column(String(100))
    about = Column(Text)
    github_url = Column(String(255))
    linkedin_url = Column(String(255))
    twitter_url = Column(String(255), nullable=True)
    profile_picture_url = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Profile(name='{self.name}', email='{self.email}')>"

    def to_dict(self):
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
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
