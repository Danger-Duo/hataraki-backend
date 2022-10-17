from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from app.utils.pydantic_object_id import PydanticObjectId


class LoginResDto(BaseModel):
    access_token: str
    token_type: str


class RegisterReqDto(BaseModel):
    email: EmailStr
    password: str
    company: str


class RegisterResDto(BaseModel):
    id: PydanticObjectId = Field(default_factory=PydanticObjectId, alias="_id")
    email: EmailStr
    company: str
    roles: list[str]
    createdAt: datetime
    updatedAt: datetime
