from fastapi import HTTPException, status

from database.models import Article, User


def check_permissions(article: Article, current_user: User) -> bool:
    if article.user_id != current_user.id:
        if current_user.is_admin or current_user.is_superadmin:
            return True
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    return True
