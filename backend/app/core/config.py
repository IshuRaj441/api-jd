from pydantic_settings import BaseSettings
from pathlib import Path
import os

class Settings(BaseSettings):
    # Project settings
    PROJECT_NAME: str = "Me-API Playground"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"
    TESTING: bool = False
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///./app.db"
    
    # Security
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    BACKEND_CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:5173",
        "https://api-jd.vercel.app"
    ]
    
    def __init__(self, **values):
        super().__init__(**values)
        
        # Handle database URL for production
        if os.getenv("RENDER"):
            db_url = os.getenv("DATABASE_URL")
            if db_url:
                if db_url.startswith("postgres://"):
                    db_url = db_url.replace("postgres://", "postgresql://", 1)
                self.SQLALCHEMY_DATABASE_URI = db_url
        
        # Ensure SQLite database directory exists
        if self.SQLALCHEMY_DATABASE_URI.startswith("sqlite"):
            db_path = self.SQLALCHEMY_DATABASE_URI.split("///")[-1]
            db_dir = os.path.dirname(db_path)
            if db_dir:
                os.makedirs(db_dir, exist_ok=True)
    
    @property
    def DATABASE_URL(self) -> str:
        return self.SQLALCHEMY_DATABASE_URI

    class Config:
        case_sensitive = True
        env_file = ".env" if os.path.exists(".env") else None
        env_file_encoding = 'utf-8'
        extra = 'allow'  # Allow extra environment variables without raising errors

settings = Settings()
