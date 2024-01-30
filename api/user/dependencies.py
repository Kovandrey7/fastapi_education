from typing import Annotated

from fastapi import HTTPException, status, Path

from api.user.crud import _get_user_by_id
from database.models import User


async def user_by_id(user_id: Annotated[int, Path]) -> User:
    user = await _get_user_by_id(user_id)
    if user is not None:
        return user

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User with id {user_id} not found.",
    )
