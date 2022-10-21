import httpx
from pydantic import EmailStr

from app.config import CONFIG


async def send_text_email(from_name: str, to_email: list[EmailStr], subject: str, text: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"https://api.mailgun.net/v3/{CONFIG.MAILGUN_DOMAIN_NAME}/messages",
            auth=("api", CONFIG.MAILGUN_API_KEY),
            data={
                "from": f"{from_name} <{CONFIG.EMAIL_FROM_ADDR}>",
                "to": to_email,
                "subject": subject,
                "text": text,
            },
        )
    return response
