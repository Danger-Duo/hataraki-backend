from datetime import datetime

from pydantic import BaseModel, EmailStr


class CreateUserReqDto(BaseModel):
    email: EmailStr
    password: str
    company: str
    roles: list[str]


class UserResDto(BaseModel):
    email: str
    company: str
    roles: list[str]
    createdAt: datetime
    updatedAt: datetime
