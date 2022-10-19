import boto3
from fastapi import APIRouter, status

from app.config import CONFIG
from app.dtos.presigned_url import (UploadPresignedUrlReqDto,
                                    UploadPresignedUrlResDto)

router = APIRouter(prefix="/api/v1/presigned-url", tags=["Presigned URL"])

s3_client = boto3.client("s3", aws_access_key_id=CONFIG.AWS_ACCESS_KEY_ID,
                         aws_secret_access_key=CONFIG.AWS_SECRET_ACCESS_KEY)


@router.post("/upload", response_model=UploadPresignedUrlResDto, status_code=status.HTTP_201_CREATED)
async def generate_upload_presigned_url(req_dto: UploadPresignedUrlReqDto):
    """
    Generate presigned URL for uploading file to S3 bucket. 
    eg. curl command to upload local file sfo.png with generated presigned URL
    curl --request PUT \
    --url 'https://hataraki-dev-1.s3.amazonaws.com/sfo.png?AWSAccessKeyId=...&Signature=...&content-type=image%2Fjpg&Expires=1666171105' \
    -H 'Content-Type: image/jpg' -T sfo.png
    """
    presigned_url = s3_client.generate_presigned_url(
        ClientMethod="put_object",
        Params={
            "Bucket": CONFIG.S3_BUCKET_NAME,
            "Key": req_dto.key,
            "ContentType": req_dto.contentType,
        },
        ExpiresIn=CONFIG.S3_PRESIGNED_URL_EXPIRY_SECONDS,
    )
    return {"presignedUrl": presigned_url}
