from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from sqlalchemy.exc import SQLAlchemyError, OperationalError
import os
import logging
from typing import Generator, Any, Optional
from contextlib import contextmanager

from app.core.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create engine with configuration based on environment
def get_engine():
    """Create and return a database engine based on the current configuration."""
    connect_args = {}
    
    # Handle SQLite specific configuration
    if settings.SQLALCHEMY_DATABASE_URI and settings.SQLALCHEMY_DATABASE_URI.startswith("sqlite"):
        connect_args = {"check_same_thread": False}
        
        # Ensure the directory exists for SQLite
        db_path = settings.SQLALCHEMY_DATABASE_URI.split("///")[-1]
        db_dir = os.path.dirname(db_path)
        if db_dir:
            os.makedirs(db_dir, exist_ok=True)
    
    try:
        engine = create_engine(
            settings.SQLALCHEMY_DATABASE_URI,
            connect_args=connect_args,
            pool_pre_ping=True,
            pool_size=10 if not settings.SQLALCHEMY_DATABASE_URI.startswith("sqlite") else 1,
            max_overflow=20 if not settings.SQLALCHEMY_DATABASE_URI.startswith("sqlite") else 0,
            echo=os.getenv("SQL_ECHO", "false").lower() == "true"
        )
        return engine
    except Exception as e:
        logger.error(f"Error creating database engine: {e}")
        raise

# Create engine
engine = get_engine()

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base: Any = declarative_base()

@contextmanager
def get_db_session() -> Generator[Session, None, None]:
    """Dependency function that yields a database session."""
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database error: {e}")
        db.rollback()
        raise
    finally:
        db.close()

# For backward compatibility
get_db = get_db_session

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
