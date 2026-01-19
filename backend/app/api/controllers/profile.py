from datetime import datetime

async def get_profile():
    return {
        "name": "Ishu Raj",
        "email": "ishuraj176@gmail.com",
        "role": "Full Stack Developer",
        "skills": ["Python", "JavaScript", "React", "Node.js", "FastAPI", "SQL"],
        "location": "India",
        "last_updated": datetime.utcnow().isoformat()
    }
