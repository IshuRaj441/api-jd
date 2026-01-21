from fastapi import FastAPI, status, Request, Response, Depends, HTTPException
from fastapi.responses import JSONResponse, FileResponse
import logging
import time
from typing import Callable, Dict, Any
from sqlalchemy.orm import Session

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from pathlib import Path

# Import the v1 API router and profile function
from app.api.v1.api import api_router
from app.api.v1.routes.profile import get_profile as v1_get_profile
from app.db.session import get_db

app = FastAPI(title="API JD")

# Configure CORS with environment variables
import os
from typing import List

# Get allowed origins from environment variable or use defaults
ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:3000,http://localhost:5173,https://api-jd.vercel.app,https://api-jd-ishuraj441.vercel.app,https://api-jd-w6op-72n027wu5-ishuraj441s-projects.vercel.app"
).split(",")

# Get origin regex from environment variable or use default
ALLOWED_ORIGIN_REGEX = os.getenv(
    "ALLOWED_ORIGIN_REGEX",
    r"https?://(localhost|api-jd.*\.vercel\.app|api-jd-ishuraj441.*\.vercel\.app|api-jd\.onrender\.com)"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_origin_regex=ALLOWED_ORIGIN_REGEX,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
    max_age=600
)

# Legacy profile endpoint for backward compatibility - must be defined before other routes
@app.get("/profile")
async def legacy_profile():
    """
    Legacy profile endpoint that returns the same data as the v1 profile endpoint.
    Maintained for backward compatibility with existing frontend clients.
    """
    try:
        # Directly return the profile data instead of trying to call the endpoint
        return {
            "id": 1,
            "name": "Ishu Raj",
            "email": "ishuraj176@gmail.com",
            "title": "Full Stack Developer",
            "location": "India",
            "about": "Passionate developer building amazing things with code.",
            "github_url": "https://github.com/IshuRaj441",
            "linkedin_url": "https://www.linkedin.com/in/ishu-raj-13b840291/",
            "portfolio_url": "https://api-jd-ishuraj441.vercel.app/",
            "created_at": "2024-01-21T00:00:00",
            "updated_at": "2024-01-21T00:00:00"
        }
    except Exception as e:
        logger.error(f"Error in legacy profile endpoint: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "status": "error",
                "message": "Failed to fetch profile",
                "details": str(e)
            }
        )

# Mount static files
static_dir = os.path.join(Path(__file__).parent.parent, "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Add request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next: Callable):
    start_time = time.time()
    
    # Log the incoming request
    logger.info(f"Incoming request: {request.method} {request.url}")
    
    # Process the request
    response = await call_next(request)
    
    # Calculate response time
    process_time = (time.time() - start_time) * 1000
    
    # Log the response
    logger.info(
        f"Request processed: {request.method} {request.url} "
        f"Status: {response.status_code} "
        f"Time: {process_time:.2f}ms"
    )
    
    return response


# Root endpoint
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse(os.path.join(static_dir, "favicon.ico"))

@app.get("/")
async def root():
    return {
        "message": "API JD backend running",
        "endpoints": {
            "health": "/health",
            "test": "/test",
            "api_docs": "/docs"
        }
    }

# Direct health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "service": "API JD",
        "timestamp": "2024-01-21T01:07:00Z"
    }

# Test endpoint
@app.get("/test")
async def test_endpoint():
    return {
        "status": "success",
        "message": "Test endpoint is working",
        "data": {
            "version": "1.0.0",
            "environment": "production"
        }
    }

# Log all registered routes
@app.on_event("startup")
async def log_routes():
    logger.info("Registered routes:")
    for route in app.routes:
        if hasattr(route, "methods") and hasattr(route, "path"):
            methods = ", ".join(route.methods) if hasattr(route, "methods") else ""
            logger.info(f"{methods} {route.path}")

# Include the v1 API router with the /api/v1 prefix
app.include_router(api_router, prefix="/api/v1")


# Add a simple route to list all available API endpoints
@app.get("/api")
async def list_endpoints():
    """List all available API endpoints"""
    endpoints = []
    for route in app.routes:
        if hasattr(route, "methods") and hasattr(route, "path"):
            methods = ", ".join(route.methods) if hasattr(route, "methods") else ""
            # Only include API endpoints (not static files, etc.)
            if route.path.startswith("/api"):
                endpoints.append({
                    "path": route.path,
                    "methods": methods,
                    "name": route.name,
                    "tags": getattr(route, "tags", [])
                })
    return {"endpoints": endpoints}
