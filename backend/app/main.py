from fastapi import FastAPI
from api.v1.api import api_router

app = FastAPI(title="API JD")

# Root endpoint
@app.get("/")
def root():
    return {"message": "API JD backend running"}

# Include API router with versioned prefix
app.include_router(api_router, prefix="/api/v1")
