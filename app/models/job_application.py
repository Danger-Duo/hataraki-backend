from datetime import datetime

from beanie import Document, Link
from pydantic import EmailStr, Field, HttpUrl
from pymongo import IndexModel

from app.constants.application_status import ApplicationStatus
from app.models.job_listing import JobListing


class JobApplication(Document):
    firstName: str
    lastName: str
    email: EmailStr
    startDate: datetime
    resumeLink: HttpUrl
    personalStatement: str
    applicationStatus: ApplicationStatus = ApplicationStatus.NEW
    jobListing: Link[JobListing]
    createdAt: datetime = Field(default_factory=datetime.now)
    updatedAt: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "jobapplications"
        indexes = [
            IndexModel("jobListing"),
            IndexModel("applicationStatus"),
        ]
