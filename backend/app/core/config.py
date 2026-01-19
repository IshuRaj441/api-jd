from pydantic_settings import BaseSettings
from typing import List
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    # Project settings
    PROJECT_NAME: str = "API JD Backend"
    VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    ENVIRONMENT: str = "development"
    TESTING: bool = False
    
    # API
    API_V1_STR: str = "/api/v1"
    API_PREFIX: str = "/api"
    DOCS_URL: str = "/docs"
    OPENAPI_URL: str = "/openapi.json"
    
    # Database configuration
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./app.db")
    TEST_DATABASE_URL: str = os.getenv("TEST_DATABASE_URL", "sqlite:///./test.db")
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
        "https://api-jd.vercel.app",
        "https://api-jd-*.vercel.app"
    ]
    
    # Rate Limiting
    RATE_LIMIT: int = int(os.getenv("RATE_LIMIT", "100"))
    RATE_LIMIT_WINDOW: int = int(os.getenv("RATE_LIMIT_WINDOW", "900"))  # 15 minutes
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Caching
    CACHE_TTL: int = int(os.getenv("CACHE_TTL", "300"))  # 5 minutes
    
    def __init__(self, **values):
        # Initialize SQLALCHEMY_DATABASE_URI from DATABASE_URL if not provided
        if 'SQLALCHEMY_DATABASE_URI' not in values and 'DATABASE_URL' in values:
            values['SQLALCHEMY_DATABASE_URI'] = values['DATABASE_URL']
            
        super().__init__(**values)
        
        # Handle database URL for production
        if os.getenv("RENDER"):
            db_url = os.getenv("DATABASE_URL")
            if db_url:
                if db_url.startswith("postgres://"):
                    db_url = db_url.replace("postgres://", "postgresql://", 1)
                self.SQLALCHEMY_DATABASE_URI = db_url
        
        # Ensure SQLite database directory exists
        if hasattr(self, 'SQLALCHEMY_DATABASE_URI') and self.SQLALCHEMY_DATABASE_URI.startswith("sqlite"):
            db_path = self.SQLALCHEMY_DATABASE_URI.split("///")[-1]
            db_dir = os.path.dirname(db_path)
            if db_dir:
                os.makedirs(db_dir, exist_ok=True)
    
    @property
    def DATABASE_URL(self) -> str:
        return getattr(self, 'SQLALCHEMY_DATABASE_URI', '')

    class Config:
        case_sensitive = True
        env_file = ".env" if os.path.exists(".env") else None
        env_file_encoding = 'utf-8'
        extra = 'allow'  # Allow extra environment variables without raising errors

settings = Settings()
