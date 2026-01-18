from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Dict, Any
import os
import platform

from app.api.deps import get_db
from app.core.config import settings

router = APIRouter()

@router.get("/health", status_code=200)
async def health_check() -> Dict[str, str]:
    """
    Health check endpoint that verifies the API is running.
    Returns a 200 status code with a simple status message.
    """
    return {"status": "ok"}
