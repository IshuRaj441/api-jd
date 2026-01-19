"""Database models package.

This module imports all SQLAlchemy models to ensure they are registered with the SQLAlchemy metadata.
"""
from app.db.models.project import Project  # noqa: F401

# This makes the models available for Alembic to discover
__all__ = ["Project"]

# Import all models here to ensure they are registered with SQLAlchemy's metadata
# This is necessary for Alembic to detect all models during migrations
