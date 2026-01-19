from fastapi import FastAPI, status
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.api import api_router

app = FastAPI(title="API JD")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Local frontend
        "https://api-jd.onrender.com",  # Backend itself
        "https://api-qzv8nceuf-ishuraj441s-projects.vercel.app",  # Frontend URL
        "https://api-qzv8nceuf-ishuraj441s-projects.vercel.app/"  # Frontend URL with trailing slash
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
def root():
    return {"message": "API JD backend running"}

# Health check redirect
@app.get("/health", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
async def health_redirect():
    return RedirectResponse(url="/api/v1/health/")

# Include API router with versioned prefix
app.include_router(api_router, prefix="/api/v1")
