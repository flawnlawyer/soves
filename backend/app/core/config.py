from pydantic_settings import BaseSettings
from typing import List
import secrets


class Settings(BaseSettings):
    # App
    APP_NAME: str = "Sōvēs"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False

    # Security
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./soves.db"

    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000"]

    # Storage
    DEFAULT_STORAGE_ADAPTER: str = "local"
    LOCAL_STORAGE_PATH: str = "./storage_data"
    MAX_FILE_SIZE_MB: int = 100

    # S3-compatible (Cloudflare R2, MinIO, AWS)
    S3_ENDPOINT_URL: str = ""
    S3_ACCESS_KEY_ID: str = ""
    S3_SECRET_ACCESS_KEY: str = ""
    S3_BUCKET_NAME: str = "soves"
    S3_REGION: str = "auto"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
