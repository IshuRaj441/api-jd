from fastapi import APIRouter
from .endpoints import profile, projects, health

api_router = APIRouter()

# Include all v1 endpoints
api_router.include_router(health.router, prefix="/health", tags=["Health"])
api_router.include_router(profile.router, prefix="/profile", tags=["Profile"])
api_router.include_router(projects.router, prefix="/projects", tags=["Projects"])
