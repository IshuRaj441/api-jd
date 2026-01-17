import time
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from app.core.config import settings
from app.api import api_router
from app.db.database import init_db

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

class NoCacheMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # Call the next middleware/route handler
        response = await call_next(request)
        
        # Add cache control headers to all responses
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0, no-transform"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        response.headers["X-Accel-Expires"] = "0"  # For Nginx
        
        # Ensure Vary headers are set to prevent caching variations
        if "Vary" not in response.headers:
            response.headers["Vary"] = "*"
        
        # Add timestamp to prevent caching
        response.headers["Last-Modified"] = "0"
        response.headers["ETag"] = 'W/"{}"'.format(int(time.time()))
        
        return response

# Add NoCacheMiddleware to prevent caching of API responses
app.add_middleware(NoCacheMiddleware)

# Set up CORS
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Initialize database on startup
@app.on_event("startup")
def startup_event():
    init_db()

# Health check endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the Me-API Playground!"}

# Include API router
app.include_router(api_router, prefix="")
