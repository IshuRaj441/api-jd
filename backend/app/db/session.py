from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

from app.core.config import settings
from app.db.base_class import Base

# Create the SQLAlchemy engine with SQLite-specific settings
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in str(settings.DATABASE_URL) else {},
    echo=settings.DEBUG
)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# We're using Base from app.db.base_class instead of creating a new one here

def get_db() -> Session:
    """
    Dependency function that yields database sessions.

    Usage in FastAPI route:

    @app.get("/items/")
    def read_items(db: Session = Depends(get_db)):
        items = db.query(Item).all()
        return items
    ```
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db() -> None:
    """Initialize database tables."""
    # Import all models here to ensure they are registered with SQLAlchemy
    from app.db.models import profile  # noqa: F401
    
    Base.metadata.create_all(bind=engine)
    
    # Log database initialization
    import logging
    logger = logging.getLogger(__name__)
    logger.info("Database tables created")
