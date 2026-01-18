from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from sqlalchemy import text
from typing import Dict, Any, Optional
import os
import sys
import platform
import traceback

from app.api.deps import get_db
from app.core.config import settings
from app.db.database import SessionLocal

router = APIRouter()

def check_database() -> Dict[str, str]:
    """Check database connection and return status."""
    try:
        db = SessionLocal()
        # Try to execute a simple query
        db.execute(text("SELECT 1"))
        db.close()
        return {"database": "ok"}
    except Exception as e:
        return {
            "database": "error",
            "error": str(e),
            "type": type(e).__name__,
            "traceback": traceback.format_exc()
        }

@router.get("/health", status_code=200)
async def health_check() -> Dict[str, Any]:
    """
    Health check endpoint that verifies the API and its dependencies are running.
    Returns detailed status information.
    """
    try:
        # Check database connection
        db_status = check_database()
        
        # Basic system info
        system_info = {
            "status": "ok" if db_status.get("database") == "ok" else "error",
            "python_version": sys.version.split()[0],
            "platform": platform.platform(),
            "environment": os.getenv("ENVIRONMENT", "development"),
            "database_url": "<hidden>" if settings.SQLALCHEMY_DATABASE_URI else "not configured"
        }
        
        # Add database status
        system_info["database_status"] = db_status
        
        # If there's an error, raise an exception with the details
        if system_info["status"] != "ok":
            raise HTTPException(
                status_code=500,
                detail=system_info
            )
            
        return system_info
        
    except Exception as e:
        # Catch any unexpected errors
        error_info = {
            "status": "error",
            "error": str(e),
            "type": type(e).__name__,
            "traceback": traceback.format_exc()
        }
        raise HTTPException(status_code=500, detail=error_info)
