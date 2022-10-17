from datetime import datetime

from beanie.odm.fields import PydanticObjectId
from pydantic import BaseModel, EmailStr, Field, HttpUrl

from app.models.joblisting import JobListing


class JobApplicationResDto(BaseModel):
    id: PydanticObjectId = Field(default_factory=PydanticObjectId, alias="_id")
    firstName: str
    lastName: str
    email: EmailStr
    startDate: datetime
    resumeLink: HttpUrl
    personalStatement: str
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


class GetJobApplicationResDto(JobApplicationResDto):
    pass


class SubmitJobApplicationResDto(JobApplicationResDto):
    pass
