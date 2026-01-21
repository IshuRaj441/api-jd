"""Initialize the database with tables.

This script drops all existing tables and creates new ones based on SQLAlchemy models.
"""
import sys
from pathlib import Path

# Add the backend directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from app.db.base_class import Base  # noqa: E402
from app.db.session import engine  # noqa: E402

def init_db() -> None:
    """Drop and recreate all database tables."""
    print("Dropping existing tables...")
    Base.metadata.drop_all(bind=engine)
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully!")

if __name__ == "__main__":
    init_db()
