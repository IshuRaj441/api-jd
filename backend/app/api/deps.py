from typing import Generator
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.core.config import settings


def get_db() -> Generator:
    """
    Dependency that provides a database session.
    Ensures the session is properly closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db),
    # For now, we'll skip authentication for simplicity
    # token: str = Depends(oauth2_scheme)
) -> dict:
    """
    Dependency to get the current authenticated user.
    In a real application, this would validate a JWT token.
    For now, returns a mock user.
    """
    # TODO: Implement proper authentication
    return {"id": 1, "is_active": True}


def get_current_active_user(
    current_user: dict = Depends(get_current_user),
) -> dict:
    """
    Dependency to get the current active user.
    Raises an exception if the user is inactive.
    """
    if not current_user.get("is_active", False):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user"
        )
    return current_user
