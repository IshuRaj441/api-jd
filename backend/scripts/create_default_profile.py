from app.db.session import SessionLocal
from app.db.models.profile import Profile
from datetime import datetime, timezone

def create_default_profile():
    db = SessionLocal()
    try:
        # Check if a profile already exists
        existing = db.query(Profile).first()
        if existing:
            print("Profile already exists. Skipping creation.")
            return existing

        # Create a default profile
        profile = Profile(
            name="Ishu Raj",
            email="ishuraj176@gmail.com",
            title="Full Stack Developer",
            location="India",
            about="Passionate developer building amazing things with code.",
            github_url="https://github.com/IshuRaj441",
            linkedin_url="https://www.linkedin.com/in/ishu-raj-13b840291/",
            twitter_url=None,  # Add this if your model has it
            profile_picture_url=None,  # Add this if your model has it
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        db.add(profile)
        db.commit()
        db.refresh(profile)
        print("Default profile created successfully!")
        return profile
    except Exception as e:
        db.rollback()
        print(f"Error creating default profile: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_default_profile()
