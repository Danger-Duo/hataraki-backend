from fastapi import APIRouter, HTTPException, status

from app.dtos.user import CreateUserReqDto
from app.models.user import User
from app.utils.auth import get_password_hash

router = APIRouter(prefix="/api/v1/internal", tags=["Internal"])


@router.post("/users", response_model=User, status_code=status.HTTP_201_CREATED, tags=["Internal"])
async def create_user(req_dto: CreateUserReqDto):
    """Creates a new user. For internal use only."""
    user = await User.find_many(User.email == req_dto.email).to_list()
    if user:
        raise HTTPException(400, "Email has already been used")
    new_user = User(
        email=req_dto.email,
        password=get_password_hash(req_dto.password),
        company=req_dto.company,
        roles=req_dto.roles,
    )
    return await new_user.save()
