from logging import Logger
from fastapi import APIRouter, Depends, HTTPException, status

from app.dtos.email import SendEmailReqDto
from app.models.user import User
from app.utils.auth import get_current_user
from app.utils.email import send_text_email
from app.utils.logger import get_logger

router = APIRouter(prefix="/email", tags=["Email"])


@router.post("", status_code=status.HTTP_204_NO_CONTENT)
async def send_email(req_dto: SendEmailReqDto, user: User = Depends(get_current_user), logger: Logger = Depends(get_logger)):
    """
    Send email. User authentication required.
    """
    response = await send_text_email(user.company, req_dto.to, req_dto.subject, req_dto.text)
    if response.status_code >= status.HTTP_400_BAD_REQUEST:
        logger.error(response.text)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email failed to send.")

    return
