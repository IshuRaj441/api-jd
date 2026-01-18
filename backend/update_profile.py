from app.db.database import SessionLocal
from app.models.models import Profile

def update_profile():
    db = SessionLocal()
    try:
        # Get the first profile (there should only be one)
        profile = db.query(Profile).first()
        
        if profile:
            # Update the profile
            profile.name = "Ishu Raj"
            profile.email = "ishuraj176@gmail.com"
            db.commit()
            print("Profile updated successfully")
        else:
            # If no profile exists, create one
            profile = Profile(
                name="Ishu Raj",
                email="ishuraj176@gmail.com",
                education="B.Tech in Computer Science and Engineering"
            )
            db.add(profile)
            db.commit()
            print("New profile created successfully")
    except Exception as e:
        print(f"Error updating profile: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    update_profile()
