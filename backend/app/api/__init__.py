from fastapi import APIRouter

# Create main API router
api_router = APIRouter()

# Import and include the v1 API router
from .v1 import api_router as v1_router

# Mount the v1 API router with the /api prefix
api_router.include_router(v1_router, prefix="/v1")
