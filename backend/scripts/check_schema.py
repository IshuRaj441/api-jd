import sqlite3
from pathlib import Path

def check_schema():
    # Get the path to the database
    db_path = Path(__file__).parent.parent / 'app.db'
    
    if not db_path.exists():
        print("Database file not found.")
        return
    
    # Connect to the database
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row  # This enables column access by name
    cursor = conn.cursor()
    
    try:
        # Get table info
        cursor.execute("PRAGMA table_info(profiles)")
        columns = cursor.fetchall()
        
        print("\nProfiles Table Schema:")
        print("-" * 50)
        print(f"{'Column':<25} {'Type':<15} {'Nullable':<10} {'Primary Key'}")
        print("-" * 50)
        
        for col in columns:
            print(f"{col['name']:<25} {col['type']:<15} {'YES' if col['notnull'] == 0 else 'NO':<10} {'YES' if col['pk'] == 1 else 'NO'}")
        
        # Get index info
        cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='index' AND tbl_name='profiles'")
        indexes = cursor.fetchall()
        
        print("\nIndexes on profiles table:")
        print("-" * 50)
        for idx in indexes:
            print(f"- {idx['name']}: {idx['sql']}")
        
        # Check sample data
        cursor.execute("SELECT * FROM profiles LIMIT 1")
        sample = cursor.fetchone()
        
        if sample:
            print("\nSample Profile Data:")
            print("-" * 50)
            for key in sample.keys():
                print(f"{key}: {sample[key]}")
        else:
            print("\nNo profile data found.")
        
    except Exception as e:
        print(f"Error checking schema: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    check_schema()
