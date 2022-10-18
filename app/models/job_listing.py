from datetime import datetime

from beanie import Document, Link
from pydantic import Field
from pymongo import IndexModel

from app.models.user import User


class JobListing(Document):
    title: str
    description: str
    location: str
    startDate: datetime
    employmentType: str
    createdBy: Link[User]
    createdAt: datetime = Field(default_factory=datetime.now)
    updatedAt: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "joblistings"
        indexes = [
            IndexModel("title"),
            IndexModel("createdBy")
        ]
