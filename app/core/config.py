import secrets
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, EmailStr, PostgresDsn, field_validator
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # API Settings #
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Financial Marketing Compliance Platform"
    PROJECT_DESCRIPTION: str = "API for financial marketing compliance review automation"
    PROJECT_VERSION: str = "1.0.0"

    # Environment #
    ENVIRONMENT: str = "development"  # development, staging, production #

    # Security #
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days #
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    # 60 minutes * 24 hours * 30 days = 30 days #
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 30

    # CORS #
    CORS_ORIGINS: List[AnyHttpUrl] = []

    @field_validator("CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    # Database #
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: str = "5432"
    DATABASE_URI: Optional[PostgresDsn] = None

    @field_validator("DATABASE_URI", mode="before")
    def assemble_db_connection(cls, v: Optional[str], info: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        
        values = info.data
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            port=values.get("POSTGRES_PORT"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )
    
    # Email Settings #
    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = None
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[EmailStr] = None
    EMAILS_FROM_NAME: Optional[str] = None
    
    # Admin User #
    FIRST_SUPERUSER: EmailStr
    FIRST_SUPERUSER_PASSWORD: str

    # Logging #
    LOG_LEVEL: str = "INFO"

    # Password Settings #
    PASSWORD_MIN_LENGTH: int = 8

    # File Storage #
    STORAGE_BUCKET: Optional[str] = None
    
    class Config:
        case_sensitive = True
        env_file = ".env"


# Create settings instance # 
settings = Settings()