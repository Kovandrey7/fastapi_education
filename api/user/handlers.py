from fastapi import APIRouter, status, HTTPException, Depends

from api.user.crud import _create_user, _delete_user, _update_user
from api.user.dependencies import user_by_id
from api.user.schemas import UserCreate, ShowUser, UserDelete, UserUpdate
from authentication.auth import get_current_user
from database.models import User
from authentication.hashed_password import get_password_hash

router = APIRouter(tags=["User"], prefix="/user")


@router.post("/", response_model=ShowUser, status_code=status.HTTP_201_CREATED)
async def create_user(user_in: UserCreate) -> ShowUser:
    hashed_password = get_password_hash(user_in.password)
    user = await _create_user(user_in=user_in, hashed_password=hashed_password)
    return ShowUser(
        id=user.id, username=user.username, email=user.email, role=user.role
    )


@router.get("/", response_model=ShowUser, status_code=status.HTTP_200_OK)
async def get_user_by_id(user: User = Depends(user_by_id)) -> ShowUser:
    return ShowUser(
        id=user.id, username=user.username, email=user.email, role=user.role
    )


@router.put("/", response_model=ShowUser, status_code=status.HTTP_200_OK)
async def update_user(
    user_in: UserUpdate, user: User = Depends(get_current_user)
) -> ShowUser:
    user_update = await _update_user(user_in=user_in, user=user)
    return ShowUser(
        id=user_update.id,
        username=user.username,
        email=user_update.email,
        role=user.role,
    )


@router.delete("/", response_model=UserDelete, status_code=status.HTTP_200_OK)
async def delete_user(user_id: int) -> UserDelete:
    deleted_user_id = await _delete_user(user_id)
    if deleted_user_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found.",
        )
    return UserDelete(deleted_user_id=deleted_user_id)
