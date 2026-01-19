from fastapi import APIRouter
from .routes import health, projects
from .endpoints import profile as profile_endpoint

# Create main API router
api_router = APIRouter()

# Include all routes
api_router.include_router(health.router, prefix="/health", tags=["Health"])
api_router.include_router(projects.router, prefix="/projects", tags=["Projects"])

# Include API v1 endpoints
v1_router = APIRouter(prefix="/v1")

# Include profile endpoint without additional prefix (it already has /profile prefix)
v1_router.include_router(profile_endpoint.router, tags=["Profile"])

# Mount v1 router with prefix
api_router.include_router(v1_router, prefix="")
