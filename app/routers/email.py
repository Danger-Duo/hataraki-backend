from logging import Logger
from fastapi import APIRouter, Depends, HTTPException, status
import httpx

from app.config import CONFIG
from app.dtos.email import SendEmailReqDto
from app.models.user import User
from app.utils.auth import get_current_user
from app.utils.logger import get_logger

router = APIRouter(prefix="/email", tags=["Email"])


@router.post("", status_code=status.HTTP_204_NO_CONTENT)
async def send_email(req_dto: SendEmailReqDto, user: User = Depends(get_current_user), logger: Logger = Depends(get_logger)):
    """
    Send email. User authentication required.
    """
    # make httpx request
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"https://api.mailgun.net/v3/{CONFIG.MAILGUN_DOMAIN_NAME}/messages",
            auth=("api", CONFIG.MAILGUN_API_KEY),
            data={
                "from": f"{user.company} <{CONFIG.EMAIL_FROM_ADDR}>",
                "to": req_dto.to,
                "subject": req_dto.subject,
                "text": req_dto.text,
            },
        )
    if response.status_code >= status.HTTP_400_BAD_REQUEST:
        logger.error(response.text)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email failed to send.")

    return
