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

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "https://api-jd.vercel.app",
        "https://api-jd-ishuraj441.vercel.app"
    ],
    allow_origin_regex=r"https?://(localhost|api-jd.*\.vercel\.app|api-jd\.onrender\.com)",
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
    Legacy profile endpoint that proxies to the new /api/v1/profile endpoint.
    Maintained for backward compatibility with existing frontend clients.
    """
    try:
        # Import the router to call the v1 profile endpoint
        from fastapi import Request
        from fastapi.responses import JSONResponse
        from fastapi import status
        
        # Create a mock request to pass to the v1 endpoint
        request = Request(scope={
            'type': 'http',
            'method': 'GET',
            'path': '/api/v1/profile',
            'headers': []
        })
        
        # Call the v1 profile endpoint through the router
        response = await api_router.routes[0].endpoint(request)
        return response
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
