from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.config import CONFIG
from app.exceptions.invalid_credentials_exception import \
    InvalidCredentialsException
from app.models.user import User

JWT_ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    return pwd_context.hash(password)


async def auth_user(email: str, password: str) -> Optional[User]:
    user = await User.find_one(User.email == email)
    if not user or not verify_password(password, user.password):
        return
    return user


def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=15)):
    """Creates a JWT access token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, CONFIG.JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt


def create_user_token(user: User) -> str:
    """Creates a JWT access token for a user"""
    access_token_expiry = timedelta(hours=CONFIG.ACCESS_TOKEN_EXPIRE_HOURS)
    return create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expiry
    )


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, CONFIG.JWT_SECRET, algorithms=[JWT_ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise InvalidCredentialsException()
    except JWTError:
        raise InvalidCredentialsException()
    user = await User.find_one(User.email == email)
    if not user:
        raise InvalidCredentialsException()
    return user
