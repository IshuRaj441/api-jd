from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError
import os
import logging
from typing import Generator, Any

from app.core.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create engine with configuration based on environment
connect_args = {}
if settings.SQLALCHEMY_DATABASE_URI.startswith("sqlite"):
    # SQLite specific configuration
    connect_args = {"check_same_thread": False}
    
engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    connect_args=connect_args,
    pool_pre_ping=True,
    pool_size=10 if not settings.SQLALCHEMY_DATABASE_URI.startswith("sqlite") else 1,
    max_overflow=20 if not settings.SQLALCHEMY_DATABASE_URI.startswith("sqlite") else 0
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base: Any = declarative_base()

def get_db() -> Generator:
    """Dependency for getting a database session.
    
    Yields:
        Session: A SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        logger.error(f"Database error: {e}")
        db.rollback()
        raise
    finally:
        db.close()

def init_db() -> None:
    """Initialize the database by creating all tables and seeding initial data.
    
    This should be called during application startup.
    """
    from .init_db import init_db as init_db_tables
    from .init_db import seed_initial_data
    
    try:
        # Initialize database tables
        init_db_tables()
        
        # Seed initial data
        seed_initial_data()
        
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise
