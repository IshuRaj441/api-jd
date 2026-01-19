from fastapi import APIRouter
from .endpoints import health, profile, projects

api_router = APIRouter()

# Include all versioned API routes
api_router.include_router(health.router, tags=["health"])
api_router.include_router(profile.router, prefix="/profile", tags=["profile"])
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
