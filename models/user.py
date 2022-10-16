from datetime import datetime

from beanie import Document, Indexed
from pydantic import EmailStr, Field


class User(Document):
    username: Indexed(str, unique=True)  # type: ignore
    password: str
    email: Indexed(EmailStr, unique=True)  # type: ignore
    company: str
    role: str
    createdAt: datetime = Field(default_factory=datetime.now)
    updatedAt: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "users"
