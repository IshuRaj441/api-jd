from app.db.database import SessionLocal, engine
from app.models.models import Profile, Base

def update_profile():
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Get the first profile (there should only be one)
        profile = db.query(Profile).first()
        
        if profile:
            # Update the profile
            profile.name = "Ishu Raj"
            profile.email = "ishuraj441@gmail.com"
            profile.education = "B.Tech (Cse), Chandigarh University — 2023–2027"
            db.commit()
            print("Profile updated successfully")
        else:
            # If no profile exists, create one
            profile = Profile(
                name="Ishu Raj",
                email="ishuraj441@gmail.com",
                education="B.Tech (Cse), Chandigarh University — 2023–2027"
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
