import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.models import Profile

def update_production_profile():
    # Get the database URL from environment variables
    database_url = os.getenv("DATABASE_URL", "sqlite:///./app.db")
    
    # Create a database connection
    engine = create_engine(database_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Get the first profile (there should only be one)
        profile = db.query(Profile).first()
        
        if profile:
            # Update the profile
            print("Updating existing profile...")
            profile.name = "Ishu Raj"
            profile.email = "ishuraj176@gmail.com"
            db.commit()
            print("Profile updated successfully")
        else:
            # If no profile exists, create one
            print("No profile found, creating a new one...")
            profile = Profile(
                name="Ishu Raj",
                email="ishuraj176@gmail.com",
                education="B.Tech in Computer Science and Engineering"
            )
            db.add(profile)
            db.commit()
            print("New profile created successfully")
            
        # Verify the update
        updated_profile = db.query(Profile).first()
        print("\nUpdated Profile:")
        print(f"Name: {updated_profile.name}")
        print(f"Email: {updated_profile.email}")
        
    except Exception as e:
        print(f"Error updating profile: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    update_production_profile()
