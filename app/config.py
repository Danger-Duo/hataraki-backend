from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    MONGO_URI: str
    JWT_SECRET: str  # required field, fails if not set
    ACCESS_TOKEN_EXPIRE_HOURS: int = 24
    S3_BUCKET_NAME: str
    S3_PRESIGNED_URL_EXPIRY_SECONDS: int = 3600
    S3_ENDPOINT_URL: Optional[str] = None
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    MAILGUN_API_KEY: str
    MAILGUN_DOMAIN_NAME: str
    EMAIL_FROM_ADDR: EmailStr
    DOMAIN_NAME: str

    class Config:
        env_file = ".env"


CONFIG = Settings()  # type: ignore


class LogConfig(BaseSettings):
    """Logging configuration to be set for the server"""

    LOGGER_NAME: str = "hataraki-backend"
    LOG_FORMAT: str = "%(levelprefix)s | %(asctime)s | %(message)s"
    LOG_LEVEL: str = "INFO"

    # Logging config
    version = 1
    disable_existing_loggers = False
    formatters = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%dT%H:%M:%S%z",
        },
    }
    handlers = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    }
    loggers = {
        "hataraki-backend": {"handlers": ["default"], "level": LOG_LEVEL},
    }
