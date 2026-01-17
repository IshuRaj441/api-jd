from fastapi import APIRouter
from .endpoints import router as api_router_v1
from .health import router as health_router

api_router = APIRouter()
api_router.include_router(health_router, tags=["health"])
api_router.include_router(api_router_v1, prefix="/api/v1")
