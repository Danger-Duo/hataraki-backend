from pydantic import BaseModel


class UploadPresignedUrlReqDto(BaseModel):
    key: str
    contentType: str


class PresignedUrlResDto(BaseModel):
    presignedUrl: str


class DownloadPresignedUrlResDto(PresignedUrlResDto):
    pass


class UploadPresignedUrlResDto(PresignedUrlResDto):
    key: str
