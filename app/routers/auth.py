from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.config import CONFIG
from app.dtos.auth import LoginResDto
from app.utils.auth import auth_user, create_access_token

router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])


@router.post("/token", response_model=LoginResDto)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await auth_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    access_token_expiry = timedelta(hours=CONFIG.ACCESS_TOKEN_EXPIRE_HOURS)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expiry
    )
    return {"access_token": access_token, "token_type": "bearer"}
