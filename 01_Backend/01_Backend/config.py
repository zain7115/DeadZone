"""
DeadZone Backend Configuration
"""
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "DeadZone API"
    VERSION: str = "0.1.0"
    API_PORT: int = 5000
    DATABASE_URL: str = "sqlite:///./deadzone.db"
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ]

settings = Settings()
