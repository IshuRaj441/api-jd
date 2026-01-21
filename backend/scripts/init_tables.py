"""Initialize database tables."""
import sys
from pathlib import Path

# Add the backend directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from app.db.base_class import Base
from app.db.session import engine
from app.db.models import profile  # noqa: F401 - Import needed for table creation

def init_tables():
    """Create all database tables."""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    init_tables()
