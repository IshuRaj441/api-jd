from fastapi import APIRouter, Query
from typing import Optional
from app.api.controllers.projects import get_projects

router = APIRouter()

@router.get("/")
async def projects(skill: Optional[str] = None):
    return await get_projects(skill)
