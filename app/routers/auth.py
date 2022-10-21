from beanie.odm.operators.update.general import Unset
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
import secrets

from app.config import CONFIG
from app.dtos.auth import LoginResDto, RegisterReqDto, RegisterResDto
from app.exceptions.invalid_credentials_exception import \
    InvalidCredentialsException
from app.models.user import User
from app.utils.auth import auth_user, create_user_token, get_password_hash
from app.utils.email import send_text_email

router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])


@router.post("/login", response_model=LoginResDto)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await auth_user(form_data.username, form_data.password)
    if not user:
        raise InvalidCredentialsException(detail="Incorrect email or password")
    if user.registrationToken:
        raise InvalidCredentialsException(detail="Please verify your email with the link sent to you")
    user_token = create_user_token(user)
    return {"access_token": user_token, "token_type": "bearer"}


@router.post("/register", response_model=RegisterResDto, status_code=status.HTTP_201_CREATED)
async def register_user(register_dto: RegisterReqDto):
    """Registers a new user"""
    # TODO: Add email validation flow
    user = await User.find_one(User.email == register_dto.email).exists()
    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email has already been used")
    hashed_pwd = get_password_hash(register_dto.password)
    user = User(
        email=register_dto.email,
        password=hashed_pwd,
        company=register_dto.company,
        registrationToken=secrets.token_urlsafe(32)
    )
    # send email confirmation to user's email
    await send_text_email(
        'Hataraki', [register_dto.email],
        'Confirm your registration on Hataraki',
        f'Please click on the link below to confirm your registration:\n\n{CONFIG.DOMAIN_NAME}/api/v1/auth/confirm-email/{user.registrationToken}')

    return await user.create()


@router.get("/confirm-email/{token}", status_code=status.HTTP_304_NOT_MODIFIED)
async def confirm_email(token: str):
    """Confirms a user's email"""
    user = await User.find_one(User.registrationToken == token)
    # TODO: add token expiry handling
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid token link")
    # remove registrationToken field from user document
    await user.update(Unset({"registrationToken": user.registrationToken}))
    # redirect to frontend login page
    return RedirectResponse(url=f"{CONFIG.DOMAIN_NAME}/login", status_code=status.HTTP_302_FOUND)
