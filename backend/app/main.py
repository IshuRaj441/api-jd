import os
import time
from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
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

# Mount static files
static_dir = os.path.join(os.path.dirname(__file__), "..", "static")
os.makedirs(static_dir, exist_ok=True)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

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
origins = [
    "https://api-jd.vercel.app",  # Production frontend
    "https://api-jd-git-main-ishuraj441.vercel.app",  # Vercel preview
    "http://localhost:3000",  # Local development
    "http://localhost:5173",  # Vite default port
    "https://api-jd.vercel.app"  # Explicitly added for the production deployment
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=r"https://api-jd(-[a-zA-Z0-9-]+)?\.vercel\.app$",  # Allow all Vercel preview URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"]
)

# Initialize database on startup
@app.on_event("startup")
def startup_event():
    # Only initialize the database structure, don't seed data
    # Seed data should be managed separately in production
    init_db()

# Favicon endpoint
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse(
        os.path.join(os.path.dirname(__file__), "static", "favicon.ico"),
        media_type="image/x-icon",
        headers={"Cache-Control": "public, max-age=86400"}
    )

# Health check endpoint
@app.get("/")
async def root():
    return {"message": "Hello, world!"}

# Include API router
app.include_router(api_router, prefix="")
