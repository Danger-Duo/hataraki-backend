from datetime import datetime

from beanie import Document, Link
from pydantic import EmailStr, Field, HttpUrl
from pymongo import ASCENDING, IndexModel

from app.models.joblisting import JobListing


class JobApplication(Document):
    firstName: str
    lastName: str
    email: EmailStr
    startDate: datetime
    resumeLink: HttpUrl
    personalStatement: str
    jobListing: Link[JobListing]
    createdAt: datetime = Field(default_factory=datetime.now)
    updatedAt: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "jobapplications"
        indexes = [
            IndexModel("jobListing")
        ]
