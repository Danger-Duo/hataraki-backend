from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    MONGO_URI: str
    JWT_SECRET: str  # required field, fails if not set
    ACCESS_TOKEN_EXPIRE_HOURS: int = 24
    S3_BUCKET_NAME: str
    S3_PRESIGNED_URL_EXPIRY_SECONDS: int = 3600
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str

    class Config:
        env_file = ".env"


CONFIG = Settings()  # type: ignore
