from fastapi import FastAPI

from api.article.handlers import router as article_router
from authentication.auth import auth_backend, fastapi_users
from authentication.schemas import UserRead, UserCreate

app = FastAPI()


app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/authentication/jwt",
    tags=["authentication"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/authentication",
    tags=["authentication"],
)

app.include_router(article_router)
