from datetime import datetime

from beanie.odm.fields import PydanticObjectId
from pydantic import BaseModel, Field


class CreatedByResDto(BaseModel):
    id: PydanticObjectId = Field(default_factory=PydanticObjectId, alias="_id")
    email: str
    company: str


class JobListingResDto(BaseModel):
    id: PydanticObjectId = Field(default_factory=PydanticObjectId, alias="_id")
    title: str
    description: str
    location: str
    startDate: datetime
    employmentType: str
    createdBy: CreatedByResDto
    createdAt: datetime
    updatedAt: datetime


class CreateJobListingReqDto(BaseModel):
    title: str
    description: str
    location: str
    startDate: datetime
    employmentType: str


class GetJobListingResDto(JobListingResDto):
    pass


class CreateJobListingResDto(JobListingResDto):
    pass
