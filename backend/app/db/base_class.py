from typing import Any, Dict, Type, TypeVar
from sqlalchemy.orm import DeclarativeBase, declared_attr
from sqlalchemy import Column, Integer, DateTime, func
from sqlalchemy.orm.decl_api import DeclarativeAttributeIntercept

ModelType = TypeVar("ModelType", bound="Base")

class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""
    id: Any
    __name__: str
    
    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
    
    # Common columns
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def to_dict(self) -> dict:
        """Convert model instance to dictionary."""
        return {
            c.name: getattr(self, c.name) for c in self.__table__.columns
        }
