from app.db.database import SessionLocal
from app.models.models import Profile

def check_profile():
    db = SessionLocal()
    try:
        profile = db.query(Profile).first()
        if profile:
            print(f"Current Profile:")
            print(f"Name: {profile.name}")
            print(f"Email: {profile.email}")
        else:
            print("No profile found in the database.")
    except Exception as e:
        print(f"Error checking profile: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_profile()
