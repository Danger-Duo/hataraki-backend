from datetime import datetime

from beanie import Document
from pydantic import EmailStr, Field
from pymongo import IndexModel


class User(Document):
    username: str
    password: str
    email: EmailStr
    company: str
    role: str
    createdAt: datetime = Field(default_factory=datetime.now)
    updatedAt: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "users"
        indexes = [
            IndexModel("username", unique=True),
            IndexModel("email", unique=True)
        ]
