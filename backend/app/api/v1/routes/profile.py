from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

@router.get("/")
async def get_profile():
    return {
        "name": "Ishu Raj",
        "email": "ishuraj441@gmail.com",
        "education": "B.Tech (Cse), Chandigarh University — 2023–2027",
        "title": "Full Stack Developer",
        "location": "India",
        "about": "Passionate developer building amazing things with code.",
        "github_url": "https://github.com/IshuRaj441",
        "linkedin_url": "https://linkedin.com/in/ishuraj176",
        "twitter_url": "https://twitter.com/ishuraj176",
        "profile_picture_url": "https://github.com/IshuRaj441.png",
        "created_at": "2024-01-19T00:00:00Z",
        "updated_at": datetime.utcnow().isoformat() + "Z"
    }
