from fastapi import APIRouter
from .routes.health import router as health_router
from .routes.profile import router as profile_router
from .routes.projects import router as projects_router

api_router = APIRouter()

api_router.include_router(health_router, prefix="/health")
api_router.include_router(profile_router, prefix="/profile")
api_router.include_router(projects_router, prefix="/projects")
