from fastapi import APIRouter

# Import all route modules
from .routes import health, profile, projects

# Create the API router for v1
api_router = APIRouter(tags=["v1"])

# Include all v1 endpoints
api_router.include_router(health.router, prefix="/health", tags=["Health"])
api_router.include_router(profile.router, prefix="/profile", tags=["Profile"])
api_router.include_router(projects.router, prefix="/projects", tags=["Projects"])

# This will create the following endpoints:
# GET /api/v1/health
# GET /api/v1/profile
# GET /api/v1/projects
