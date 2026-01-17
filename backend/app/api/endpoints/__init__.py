from fastapi import APIRouter
from . import profile, project, skill

router = APIRouter()
router.include_router(profile.router, tags=["profile"])
router.include_router(project.router, tags=["projects"])
router.include_router(skill.router, tags=["skills"])
