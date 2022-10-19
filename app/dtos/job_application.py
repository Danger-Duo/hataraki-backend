from datetime import datetime

from beanie.odm.fields import PydanticObjectId
from pydantic import BaseModel, EmailStr, Field, HttpUrl

from app.constants.application_status import ApplicationStatus
from app.models.job_listing import JobListing


class JobApplicationResDto(BaseModel):
    id: PydanticObjectId = Field(default_factory=PydanticObjectId, alias="_id")
    firstName: str
    lastName: str
    email: EmailStr
    startDate: datetime
    resumeLink: HttpUrl
    personalStatement: str
    applicationStatus: ApplicationStatus
    jobListing: JobListing
    createdAt: datetime
    updatedAt: datetime


class SubmitJobApplicationReqDto(BaseModel):
    firstName: str
    lastName: str
    email: EmailStr
    startDate: datetime
    resumeLink: HttpUrl
    personalStatement: str


class UpdateJobApplicationStatusReqDto(BaseModel):
    applicationStatus: ApplicationStatus


class GetJobApplicationResDto(JobApplicationResDto):
    pass


class SubmitJobApplicationResDto(JobApplicationResDto):
    pass


class UpdateJobApplicationStatusResDto(JobApplicationResDto):
    pass
