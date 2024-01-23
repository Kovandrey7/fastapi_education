from fastapi import HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy import select

from authentication.security import verify_password
from config import settings
from database.db_helper import db_helper
from database.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/login")


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


async def get_current_user(request: Request):
    access_token: str = request.cookies.get("access_token")

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if access_token is None:
        raise credentials_exception
    try:
        payload = jwt.decode(
            access_token,
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


async def get_current_user_with_refresh_token(request: Request):
    refresh_token: str = request.cookies.get("refresh_token")

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            refresh_token,
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
