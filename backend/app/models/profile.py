from sqlalchemy import Column, String, Text, JSON
from .base import BaseModel

class Profile(BaseModel):
    __tablename__ = 'profile'
    
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    education = Column(Text, nullable=True)
    bio = Column(Text, nullable=True)
    
    # Social/Professional Links
    links = Column(JSON, default={
        'github': '',
        'linkedin': '',
        'portfolio': '',
        'twitter': ''
    })
    
    # Additional fields that might be useful
    location = Column(String(200), nullable=True)
    headline = Column(String(200), nullable=True)
    
    def __repr__(self):
        return f"<Profile(id={self.id}, name='{self.name}', email='{self.email}')>"
