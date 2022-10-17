from typing import Union

from fastapi import APIRouter, Depends

from app.dtos.user import UserResDto
from app.models.user import User
from app.utils.auth import get_current_user

router = APIRouter(prefix="/api/v1/users", tags=["User"])


@router.get("/", response_model=list[UserResDto])
async def search_users(email: Union[str, None] = None, company: Union[str, None] = None):
    """Returns all users with optional filters"""
    search_criteria = {}
    if email:
        search_criteria["email"] = email
    if company:
        search_criteria["company"] = company
    return await User.find(search_criteria).to_list()


@router.get("/me", response_model=User)
async def get_me(user: User = Depends(get_current_user)):
    """Returns current user"""
    return user
