from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    MONGO_URI: Optional[str] = None
    JWT_SECRET: str  # required field, fails if not set
    ACCESS_TOKEN_EXPIRE_HOURS: int = 24

    class Config:
        env_file = ".env"


CONFIG = Settings()  # type: ignore
