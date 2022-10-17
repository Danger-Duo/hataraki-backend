from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from app.utils.pydantic_object_id import PydanticObjectId


class CreatedByResDto(BaseModel):
    id: PydanticObjectId = Field(default_factory=PydanticObjectId, alias="_id")
    email: str
    company: str

    class Settings:
        projection = {"_id": 1, "company": 1, "email": 1}


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
