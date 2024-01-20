from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy import select

from authentication.hashed_password import verify_password
from config import settings
from database.db_helper import db_helper
from database.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/token")


async def _get_user_by_email(email: str) -> User:
    async with db_helper.session_factory() as session:
        query = select(User).where(User.email == email)
        user = await session.scalar(query)
        if user is not None:
            return user


async def authenticate_user(email: str, password: str):
    user = await _get_user_by_email(email=email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await _get_user_by_email(email=email)
    if user is None:
        raise credentials_exception
    return user
