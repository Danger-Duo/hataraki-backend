import logging
from fastapi import APIRouter, Depends, HTTPException, status
import httpx

from app.config import CONFIG
from app.dtos.email import SendEmailReqDto
from app.models.user import User
from app.utils.auth import get_current_user

router = APIRouter(prefix="/email", tags=["Email"])


@router.post("")
async def send_email(req_dto: SendEmailReqDto, user: User = Depends(get_current_user)):
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
        logging.error(response.text)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email failed to send.")

    return {"message": f"Email successfully sent."}
