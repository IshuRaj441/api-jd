import sqlite3
import os
from pathlib import Path

def cleanup_database():
    # Get the path to the database
    db_path = Path(__file__).parent.parent / 'app.db'
    
    if not db_path.exists():
        print("Database file not found. No cleanup needed.")
        return
    
    # Connect to the database
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    try:
        # List all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print("Current tables in database:")
        for table in tables:
            print(f"- {table[0]}")
        
        # Drop problematic tables
        tables_to_drop = ['profiles_new', 'profiles_old']
        for table in tables_to_drop:
            cursor.execute(f"DROP TABLE IF EXISTS {table}")
            print(f"Dropped table: {table}")
        
        # Commit changes
        conn.commit()
        print("\nCleanup completed successfully.")
        
    except Exception as e:
        print(f"Error during cleanup: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    cleanup_database()
