from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Dict, Any

from app.api.deps import get_db
from app.core.config import settings

router = APIRouter()

@router.get("/health", response_model=Dict[str, Any])
async def health_check(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    Health check endpoint that verifies the API and database are running.
    Returns a 200 status code if everything is working correctly.
    """
    # Test database connection
    db.execute("SELECT 1")
    
    return {
        "status": "ok",
        "environment": settings.ENVIRONMENT,
        "testing": settings.TESTING,
        "database": "connected"
    }
