from pydantic_settings import BaseSettings
from pathlib import Path
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "Me-API Playground"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # Database configuration
    if os.getenv("RENDER"):
        # Production settings for Render
        DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./app.db")
        if DATABASE_URL.startswith("postgres://"):
            DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    else:
        # Development settings
        DATABASE_URL: str = "sqlite:///./app.db"
    
    # Ensure the database directory exists
    if DATABASE_URL.startswith("sqlite"):
        db_path = DATABASE_URL.split("///")[-1]
        db_dir = os.path.dirname(db_path)
        if db_dir:
            os.makedirs(db_dir, exist_ok=True)
    
    BACKEND_CORS_ORIGINS: list = os.getenv(
        "BACKEND_CORS_ORIGINS", 
        "http://localhost:3000,http://localhost:5173,https://api-jd.vercel.app"
    ).split(",")

    class Config:
        case_sensitive = True
        env_file = ".env" if os.path.exists(".env") else None

settings = Settings()
