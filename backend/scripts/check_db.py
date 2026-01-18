import os
import sys
from pathlib import Path
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

# Database URL - use the same as in your settings
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

def check_database():
    print(f"Connecting to database: {DATABASE_URL}")
    
    try:
        # Create engine
        engine = create_engine(DATABASE_URL)
        
        # Create a session
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # Test connection
        print("Testing database connection...")
        result = db.execute(text("SELECT 1"))
        print(f"Database connection successful. Result: {result.scalar()}")
        
        # Check if tables exist
        print("\nChecking tables:")
        result = db.execute(text("SELECT name FROM sqlite_master WHERE type='table';"))
        tables = [row[0] for row in result.fetchall()]
        
        if not tables:
            print("No tables found in the database!")
        else:
            print("Found tables:", ", ".join(tables))
            
            # For each table, count rows
            for table in tables:
                try:
                    count = db.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar()
                    print(f"- {table}: {count} rows")
                except Exception as e:
                    print(f"- {table}: Error - {str(e)}")
        
        db.close()
        
    except Exception as e:
        print(f"Error connecting to database: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    print("=== Database Check Utility ===\n")
    check_database()
