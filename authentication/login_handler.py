from datetime import timedelta, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm

from authentication.auth import (
    authenticate_user,
    get_current_user,
    get_current_user_with_refresh_token,
)
from authentication.schemas import Token
from authentication.security import create_access_token, create_refresh_token
from config import settings
from database.models import User

login_router = APIRouter(tags=["Login"], prefix="/login")


@login_router.post("/login", status_code=status.HTTP_200_OK)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], response: Response
) -> Token:
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    refresh_token = create_refresh_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES),
    )
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True)
    return Token(
        access_token=access_token, refresh_token=refresh_token, token_type="bearer"
    )


@login_router.post("/refresh", status_code=status.HTTP_200_OK)
async def refresh_access_token(
    response: Response,
    current_user: Annotated[User, Depends(get_current_user_with_refresh_token)],
):
    access_token = create_access_token(
        data={"sub": current_user.email},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    refresh_token = create_refresh_token(
        data={"sub": current_user.email},
        expires_delta=timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES),
    )
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True)
    return Token(
        access_token=access_token, refresh_token=refresh_token, token_type="bearer"
    )


@login_router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(
    response: Response, current_user: Annotated[User, Depends(get_current_user)]
):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"status": "Logout successfully"}
