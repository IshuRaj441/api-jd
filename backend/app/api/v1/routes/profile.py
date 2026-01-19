from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_profile():
    return {
        "name": "Ishu Raj",
        "email": "ishuraj176@gmail.com"
    }
