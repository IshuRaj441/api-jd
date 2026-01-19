from fastapi import APIRouter
from app.api.controllers.health import get_health

router = APIRouter()

@router.get("/")
async def health():
    return await get_health()
