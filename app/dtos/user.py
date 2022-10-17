from datetime import datetime

from beanie.odm.fields import PydanticObjectId
from pydantic import BaseModel, EmailStr, Field


class CreateUserReqDto(BaseModel):
    email: EmailStr
    password: str
    company: str
    roles: list[str]


class UserResDto(BaseModel):
    id: PydanticObjectId = Field(default_factory=PydanticObjectId, alias="_id")
    email: EmailStr
    company: str
    roles: list[str]
    createdAt: datetime
    updatedAt: datetime
