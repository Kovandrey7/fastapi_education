from fastapi import FastAPI

from api.article.handlers import router as article_router
from api.user.handlers import router as user_router
from authentication.login_handler import login_router

app = FastAPI()


app.include_router(login_router)
app.include_router(user_router)
app.include_router(article_router)
