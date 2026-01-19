from fastapi import APIRouter, Depends
from app.api.controllers.profile import get_profile

router = APIRouter()

@router.get("/")
async def profile():
    return await get_profile()
