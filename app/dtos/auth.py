from pydantic import BaseModel


class LoginResDto(BaseModel):
    access_token: str
    token_type: str
