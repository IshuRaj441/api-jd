from fastapi import APIRouter, Depends
from typing import Dict, Any
from datetime import datetime

router = APIRouter()

@router.get("/", response_model=Dict[str, Any])
async def health_check() -> Dict[str, Any]:
    """
    Health check endpoint that returns the current status of the API.
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }
