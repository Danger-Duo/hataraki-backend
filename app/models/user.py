from datetime import datetime
from typing import Optional

from beanie import Document
from pydantic import EmailStr, Field
from pymongo import IndexModel


class User(Document):
    email: EmailStr
    password: str
    company: str
    roles: list[str] = Field(default=['user'])
    registrationToken: Optional[str] = None
    createdAt: datetime = Field(default_factory=datetime.now)
    updatedAt: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "users"
        indexes = [
            IndexModel("email", unique=True)
        ]
