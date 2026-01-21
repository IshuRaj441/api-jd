from app.db.session import SessionLocal
from app.db.models.profile import Profile

def list_profiles():
    db = SessionLocal()
    try:
        profiles = db.query(Profile).all()
        if not profiles:
            print("No profiles found in the database.")
        for profile in profiles:
            print(f"ID: {profile.id}, Name: {profile.name}, Email: {profile.email}")
    except Exception as e:
        print(f"Error accessing database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    list_profiles()
