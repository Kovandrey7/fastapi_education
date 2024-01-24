from sqlalchemy import update, select

from api.user.schemas import UserCreate, UserUpdate, RolesUpdate
from database.db_helper import db_helper
from database.models import User


async def _create_user(user_in: UserCreate, hashed_password: str) -> User:
    async with db_helper.session_factory() as session:
        new_user = User(
            username=user_in.username,
            email=user_in.email,
            hashed_password=hashed_password,
        )
        session.add(new_user)
        await session.commit()
        return new_user


async def _get_user_by_id(user_id: int) -> User:
    async with db_helper.session_factory() as session:
        query = select(User).where(User.id == user_id, User.is_active == True)
        user = await session.scalar(query)
        if user is not None:
            return user


async def _update_user(data: UserUpdate | RolesUpdate, user: User) -> User:
    async with db_helper.session_factory() as session:
        stmt = (
            update(User)
            .where(User.id == user.id)
            .values(**data.model_dump(exclude_none=True))
            .returning(User)
        )
        user_update = await session.scalar(stmt)
        await session.commit()
        if user_update is not None:
            return user_update


async def _delete_user(user_id: int) -> int | None:
    async with db_helper.session_factory() as session:
        stmt = (
            update(User)
            .where(User.id == user_id, User.is_active == True)
            .values(is_active=False)
            .returning(User.id)
        )
        deleted_user_id = await session.scalar(stmt)
        await session.commit()
        if deleted_user_id is not None:
            return deleted_user_id
