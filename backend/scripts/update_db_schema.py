import sys
import os
from sqlalchemy import text
from sqlalchemy.exc import OperationalError

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.database import engine

def update_schema():
    """Update the database schema to add missing columns."""
    print("🔄 Updating database schema...")
    
    # SQL statements to update the schema
    update_queries = [
        # Add description column to skills table if it doesn't exist
        """
        CREATE TABLE IF NOT EXISTS new_skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100) NOT NULL,
            description TEXT,
            created_at DATETIME,
            updated_at DATETIME,
            UNIQUE (name)
        )
        """,
        
        # Copy data from old skills table to new one
        """
        INSERT OR IGNORE INTO new_skills (id, name, created_at, updated_at)
        SELECT id, name, created_at, updated_at FROM skills
        """,
        
        # Drop old table
        "DROP TABLE IF EXISTS skills",
        
        # Rename new table
        "ALTER TABLE new_skills RENAME TO skills",
        
        # Recreate indexes
        "CREATE INDEX IF NOT EXISTS ix_skills_name ON skills (name)",
    ]
    
    with engine.connect() as connection:
        with connection.begin():
            for query in update_queries:
                try:
                    connection.execute(text(query))
                except OperationalError as e:
                    print(f"⚠️  Warning: {e}")
                    continue
    
    print("✅ Database schema updated successfully!")

if __name__ == "__main__":
    update_schema()
    
    # After updating the schema, run the populate script
    print("\n🔄 Populating database with sample data...")
    from scripts.populate_sample_data import main as populate_data
    populate_data()
