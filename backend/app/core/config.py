from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Me-API Playground"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = "sqlite:///./app.db"
    BACKEND_CORS_ORIGINS: list = ["*"]  # For development only

    class Config:
        case_sensitive = True

settings = Settings()
