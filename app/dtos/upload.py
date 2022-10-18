from pydantic import BaseModel


class UploadPresignedUrlReqDto(BaseModel):
    key: str
    contentType: str


class UploadPresignedUrlResDto(BaseModel):
    presignedUrl: str
