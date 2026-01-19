from fastapi import APIRouter
from .endpoints import project, profile
from .health import router as health_router

# Create main API router
api_router = APIRouter()

# Include health check endpoint
api_router.include_router(health_router, tags=["health"])

# Include API v1 endpoints
v1_router = APIRouter(prefix="/api/v1")

# Include project and profile endpoints
v1_router.include_router(project.router, tags=["projects"])
v1_router.include_router(profile.router, tags=["profile"])

# Mount v1 router with prefix
api_router.include_router(v1_router, prefix="")
