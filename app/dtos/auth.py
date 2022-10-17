from pydantic import BaseModel, EmailStr

from app.models.user import User


class LoginResDto(BaseModel):
    access_token: str
    token_type: str


class RegisterReqDto(BaseModel):
    email: EmailStr
    password: str
    company: str


class RegisterResDto(User):
    pass
