from fastapi import APIRouter
from .routes import health, profile
from .endpoints import projects  # Keep other endpoint imports as is

# Create the API router for v1
api_router = APIRouter(tags=["v1"])

# Include all v1 endpoints with their respective prefixes
api_router.include_router(health.router, prefix="/health", tags=["Health"])
# Include the profile router from routes
api_router.include_router(profile.router, prefix="/profile", tags=["Profile"])
api_router.include_router(projects.router, prefix="/projects", tags=["Projects"])

# This will create the following endpoints:
# GET /api/v1/health
# GET /api/v1/profile
# GET /api/v1/projects
