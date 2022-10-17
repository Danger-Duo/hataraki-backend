from fastapi import APIRouter, Depends

from app.dtos.user import UserResDto
from app.models.user import User
from app.utils.auth import get_current_user

router = APIRouter(prefix="/api/v1/users", tags=["User"])


@router.get("/", response_model=list[UserResDto])
async def get_all_users():
    """Returns all users"""
    return await User.find_all().to_list()


@router.get("/me", response_model=User)
async def get_me(user: User = Depends(get_current_user)):
    """Returns current user"""
    return user
