from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    MONGO_URI: Optional[str] = None

    class Config:
        env_file = ".env"


CONFIG = Settings()  # init Singleton config
