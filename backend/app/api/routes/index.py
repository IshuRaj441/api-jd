from fastapi import APIRouter
from app.api.controllers.index import get_root

router = APIRouter()

@router.get("/")
async def root():
    return await get_root()
