import boto3
from fastapi import APIRouter, Depends, HTTPException, status

from app.config import CONFIG
from app.dtos.presigned_url import (DownloadPresignedUrlResDto,
                                    UploadPresignedUrlReqDto,
                                    UploadPresignedUrlResDto)
from app.models.user import User
from app.utils.auth import get_current_user

router = APIRouter(prefix="/api/v1/presigned-url", tags=["Presigned URL"])

s3_client = boto3.client("s3", aws_access_key_id=CONFIG.AWS_ACCESS_KEY_ID,
                         aws_secret_access_key=CONFIG.AWS_SECRET_ACCESS_KEY,
                         endpoint_url=CONFIG.S3_ENDPOINT_URL)


@router.get("", response_model=DownloadPresignedUrlResDto)
def generate_download_presigned_url(key: str, user: User = Depends(get_current_user)):
    """
    Generate a presigned URL to retrieve a private object. User authentication required.
    """
    # check if key exist in s3
    if not check_key_exist_in_s3(key):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Object not found")

    # generate presigned url
    presigned_url = s3_client.generate_presigned_url(
        ClientMethod="get_object",
        Params={"Bucket": CONFIG.S3_BUCKET_NAME, "Key": key},
        ExpiresIn=CONFIG.S3_PRESIGNED_URL_EXPIRY_SECONDS,
    )
    return {"presignedUrl": presigned_url}


@router.post("/upload", response_model=UploadPresignedUrlResDto, status_code=status.HTTP_201_CREATED)
def generate_upload_presigned_url(req_dto: UploadPresignedUrlReqDto):
    """
    Generate presigned URL for uploading file to S3 bucket. Eg curl command to upload local file with generated presigned URL
    curl --request PUT --url 'https://hataraki-dev-1.s3.amazonaws.com/myfile.png?AWSAccessKeyId=...&Signature=...&content-type=image%2Fpng&Expires=1666171105' \
    -H 'Content-Type: image/png' -T myfile.png
    """
    # check if key exist in s3
    if check_key_exist_in_s3(req_dto.key):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Object already exist")

    try:
        presigned_url = s3_client.generate_presigned_url(
            ClientMethod="put_object",
            Params={
                "Bucket": CONFIG.S3_BUCKET_NAME,
                "Key": req_dto.key,
                "ContentType": req_dto.contentType,
            },
            ExpiresIn=CONFIG.S3_PRESIGNED_URL_EXPIRY_SECONDS,
        )
    except s3_client.exceptions.ClientError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return {"presignedUrl": presigned_url, "key": req_dto.key}


def check_key_exist_in_s3(key):
    try:
        s3_client.head_object(Bucket=CONFIG.S3_BUCKET_NAME, Key=key)
        return True
    except s3_client.exceptions.ClientError:
        return False
