import os
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_DB_PATH = os.path.join(BASE_DIR, "saarthi.db").replace("\\", "/")

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.path.join(BASE_DIR, ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

    APP_NAME: str = "SAARTHI"
    APP_ENV: str = "development"
    APP_HOST: str = "127.0.0.1"
    APP_PORT: int = 8000
    API_V1_PREFIX: str = "/api/v1"

    # Database: Supports SQLite (absolute path default) or PostgreSQL
    DATABASE_URL: str = f"sqlite:///{DEFAULT_DB_PATH}"

    FRONTEND_URL: str = "http://localhost:3000"
    CORS_ORIGINS: str = "http://localhost:3000,http://127.0.0.1:3000"

    # Sarvam AI
    SARVAM_API_KEY: str = ""
    SARVAM_BASE_URL: str = "https://api.sarvam.ai"
    SARVAM_CHAT_MODEL: str = "sarvam-105b-conversations"
    SARVAM_STT_MODEL: str = "saaras:v2"
    SARVAM_TTS_MODEL: str = "bulbul:v2"

    # Admin bootstrap & Auth
    ADMIN_BOOTSTRAP_EMAIL: str = "admin@saarthi.local"
    ADMIN_BOOTSTRAP_PASSWORD: str = "AdminSecurePassword123!"
    JWT_SECRET_KEY: str = "saarthi_super_secure_jwt_dev_key_2026_dev_only"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

settings = Settings()
