from fastapi import APIRouter, Depends, status

from app.dtos.user import CreateUserReqDto, UserResDto
from app.models.user import User
from app.utils.auth import get_current_user, get_password_hash

router = APIRouter(prefix="/api/v1/users", tags=["User"])


@router.get("/", response_model=list[UserResDto])
async def get_all_users():
    """Returns all users"""
    return await User.find_all().to_list()


@router.get("/me", response_model=User)
async def get_me(user: User = Depends(get_current_user)):
    """Returns current user"""
    return user


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED, tags=["Internal"])
async def insert_user(reqBody: CreateUserReqDto):
    """Inserts a new user into the database. For internal use only."""
    new_user = User(
        username=reqBody.username,
        password=get_password_hash(reqBody.password),
        email=reqBody.email,
        company=reqBody.company,
        role=reqBody.role,
    )
    return await new_user.save()
