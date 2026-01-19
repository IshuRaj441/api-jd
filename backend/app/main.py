import time
import logging
from fastapi import FastAPI, Request
from fastapi.middleware import Middleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Any, Dict, List, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI()

# Simple test endpoint
@app.get("/")
async def read_root():
    return {"message": "Welcome to the API JD Backend"}

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "ok"}

# Health check endpoint
@app.get("/api/health")
async def health_check():
    return {"status": "ok", "version": "1.0.0"}

# Health check endpoint is now properly namespaced under /api/health

# NoCacheMiddleware
class NoCacheMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Call the next middleware/route handler
        response = await call_next(request)
        
        # Add security headers
        response.headers.update({
            "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0, no-transform",
            "Pragma": "no-cache",
            "Expires": "0",
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block",
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
            "Content-Security-Policy": "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net; style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; img-src 'self' data: https://fastapi.tiangolo.com; font-src 'self' data: https://cdn.jsdelivr.net; connect-src 'self' https://cdn.jsdelivr.net;"
        })
        
        # Ensure Vary headers are set to prevent caching variations
        if "Vary" not in response.headers:
            response.headers["Vary"] = "Accept-Encoding"
            
        response.headers["ETag"] = 'W/"{}"'.format(int(time.time()))
        
        return response

# Add NoCacheMiddleware
app.add_middleware(NoCacheMiddleware)

# Logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    # Skip logging for health checks
    if request.url.path in ["/api/health", "/api/v1/health"]:
        return await call_next(request)
        
    start_time = time.time()
    
    # Log request
    logger.info(
        "Request started",
        extra={
            "request": {
                "method": request.method,
                "url": str(request.url),
                "headers": dict(request.headers),
                "query_params": dict(request.query_params),
                "client": f"{request.client.host}:{request.client.port}"
            }
        }
    )
    
    try:
        response = await call_next(request)
        
        # Calculate process time
        process_time = (time.time() - start_time) * 1000
        
        # Log response
        logger.info(
            "Request completed",
            extra={
                "status_code": response.status_code,
                "process_time_ms": round(process_time, 2),
                "response_headers": dict(response.headers)
            }
        )
        
        # Add response time header
        response.headers["X-Process-Time"] = f"{process_time:.2f}ms"
        
        return response
        
    except Exception as e:
        # Log the exception
        logger.error(
            "Request failed",
            exc_info=True,
            extra={
                "error": str(e),
                "traceback": str(e.__traceback__)
            }
        )
        
        # Return a 500 error
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": "Internal server error",
                "error_code": "internal_server_error"
            }
        )

# Health check endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to the API JD Backend",
        "documentation": "/api/docs",
        "version": "1.0.0"
    }

@app.get("/api")
async def api_root():
    return {
        "message": "Welcome to the API",
        "endpoints": {
            "v1": "/api/v1",
            "docs": "/api/docs",
            "health": "/api/health"
        }
    }

@app.get("/api/v1")
async def v1_root():
    return {
        "message": "Welcome to API v1",
        "endpoints": {
            "profile": "/api/v1/profile",
            "projects": "/api/v1/projects",
            "health": "/api/v1/health"
        }
    }

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=204)

# Debug endpoint to list all routes
@app.get("/api/debug/routes")
async def list_routes():
    """List all available API routes"""
    routes = []
    for route in app.routes:
        if hasattr(route, "path"):
            routes.append({
                "path": route.path,
                "name": route.name,
                "methods": getattr(route, "methods", None)
            })
    return {"routes": routes}

# API routes are already included with proper prefixes above
