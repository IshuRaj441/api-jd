import time
import logging
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Dict, Any, Optional
import os

from app.core.config import settings
from app.core.errors import register_exception_handlers, APIError
from app.api.v1.api import api_router as v1_router

# Configure logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app with metadata
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API for Job Description Management System",
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json" if settings.DEBUG else None,
    docs_url=settings.DOCS_URL if settings.DEBUG else None,
    redoc_url=None,
)

# Security headers middleware
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        security_headers = {
            "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0, no-transform",
            "Pragma": "no-cache",
            "Expires": "0",
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block",
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
            "Content-Security-Policy": "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self' data:;"
        }
        
        # Add security headers to response
        for header, value in security_headers.items():
            response.headers[header] = value
            
        # Ensure Vary headers are set to prevent caching variations
        if "Vary" not in response.headers:
            response.headers["Vary"] = "Accept-Encoding"
            
        return response

# Request logging middleware
class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Skip logging for health checks
        if request.url.path in [f"{settings.API_V1_STR}/health"]:
            return await call_next(request)
            
        start_time = time.time()
        
        # Log request
        logger.info(
            "Request started",
            extra={
                "request": {
                    "method": request.method,
                    "path": request.url.path,
                    "query_params": dict(request.query_params),
                    "client": f"{request.client.host}" if request.client else "unknown"
                }
            }
        )
        
        try:
            response = await call_next(request)
            process_time = (time.time() - start_time) * 1000
            
            # Log response
            logger.info(
                "Request completed",
                extra={
                    "method": request.method,
                    "path": request.url.path,
                    "status_code": response.status_code,
                    "process_time_ms": round(process_time, 2),
                }
            )
            
            return response
            
        except Exception as e:
            process_time = (time.time() - start_time) * 1000
            logger.error(
                "Request failed",
                exc_info=True,
                extra={
                    "method": request.method,
                    "path": request.url.path,
                    "process_time_ms": round(process_time, 2),
                }
            )
            raise

# Add middleware
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(LoggingMiddleware)

# Add CORS middleware
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Add GZip middleware for compressing responses
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Add trusted hosts middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.ALLOWED_HOSTS,
)

# Register exception handlers
app = register_exception_handlers(app)

# Root endpoint
@app.get("/")
async def root() -> Dict[str, str]:
    return {
        "name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "docs": "/docs" if settings.DEBUG else None
    }

# Health check endpoint (versioned)
@app.get(f"{settings.API_V1_STR}/health")
async def health_check() -> Dict[str, Any]:
    return {
        "status": "ok",
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "timestamp": time.time()
    }

# Include API routers
app.include_router(v1_router, prefix=settings.API_V1_STR)

# Debug endpoint to list all routes (only in development)
if settings.DEBUG:
    @app.get("/debug/routes")
    async def list_routes() -> Dict[str, Any]:
        url_list = [
            {
                "path": route.path, 
                "name": route.name,
                "methods": list(route.methods)
            }
            for route in app.routes
            if hasattr(route, "path")
        ]
        return {"routes": url_list}
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
