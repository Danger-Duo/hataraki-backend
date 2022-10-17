from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.config import CONFIG
from app.dtos.auth import LoginResDto, RegisterReqDto, RegisterResDto
from app.models.user import User
from app.utils.auth import auth_user, create_access_token, get_password_hash

router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])


@router.post("/login", response_model=LoginResDto)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await auth_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    access_token_expiry = timedelta(hours=CONFIG.ACCESS_TOKEN_EXPIRE_HOURS)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expiry
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=RegisterResDto, status_code=status.HTTP_201_CREATED)
async def register_user(register_dto: RegisterReqDto):
    """Registers a new user"""
    # TODO: Add email validation flow
    user = await User.find_many(User.email == register_dto.email).to_list()
    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email has already been used")
    hashed_pwd = get_password_hash(register_dto.password)
    user = User(
        email=register_dto.email,
        password=hashed_pwd,
        company=register_dto.company
    )
    return await user.create()
