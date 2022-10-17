from datetime import datetime

from pydantic import BaseModel, EmailStr


class CreateUserReqDto(BaseModel):
    username: str
    password: str
    email: EmailStr
    company: str
    role: str


class UserResDto(BaseModel):
    username: str
    email: str
    company: str
    role: str
    createdAt: datetime
    updatedAt: datetime
