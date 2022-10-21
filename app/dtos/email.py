from pydantic import BaseModel, EmailStr


class SendEmailReqDto(BaseModel):
    to: list[EmailStr]
    subject: str
    text: str
