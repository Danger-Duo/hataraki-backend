from pydantic import BaseModel


class UploadPresignedUrlReqDto(BaseModel):
    key: str


class PresignedUrlResDto(BaseModel):
    presignedUrl: str


class DownloadPresignedUrlResDto(PresignedUrlResDto):
    pass


class UploadPresignedUrlResDto(PresignedUrlResDto):
    fields: dict
