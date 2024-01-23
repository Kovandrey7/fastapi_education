from fastapi import HTTPException, status

from api.user.crud import _get_user_by_id
from database.models import User


async def check_user_permissions_for_delete(
    target_user_id: int, current_user: User
) -> bool:
    if current_user.id == target_user_id and current_user.is_superadmin:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Superadmin cannot be deleted via API.",
        )

    if current_user.id == target_user_id:
        return True

    if current_user.id != target_user_id:
        if current_user.is_admin or current_user.is_superadmin:
            user_for_deletion = await _get_user_by_id(user_id=target_user_id)
            if user_for_deletion is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"User with id {target_user_id} not found.",
                )
            if user_for_deletion.is_superadmin:
                raise HTTPException(
                    status_code=406, detail="Superadmin cannot be deleted via API."
                )

            if current_user.is_admin and user_for_deletion.is_admin:
                return False

            return True

        return False
