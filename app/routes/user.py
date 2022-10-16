from fastapi import APIRouter, Depends, Response

from ..models.user import User, GetUserResDto
from ..util.current_user import current_user

router = APIRouter(prefix="/user", tags=["User"])


@router.get("", response_model=GetUserResDto)
async def get_user(user: User = Depends(current_user)):
    """Returns the current user"""
    return user
