from fastapi import APIRouter, Depends, status

from api.article.crud import (
    _create_article,
    _get_articles,
    _update_article,
    _delete_article,
)
from api.article.dependencies import article_by_id
from api.article.schemas import (
    ArticleCreate,
    ArticleUpdate,
    ShowArticle,
)
from authentication.auth import current_user
from database.models import User, Article

router = APIRouter(tags=["Article"], prefix="/article")


@router.post("/", response_model=ShowArticle, status_code=status.HTTP_201_CREATED)
async def create_article(article_in: ArticleCreate, user: User = Depends(current_user)):
    return await _create_article(article_in=article_in, user_id=user.id)


@router.get("/", response_model=list[ShowArticle], status_code=status.HTTP_200_OK)
async def get_articles():
    return await _get_articles()


@router.get(
    "/{article_id}/", response_model=ShowArticle, status_code=status.HTTP_200_OK
)
async def get_article_by_id(article: Article = Depends(article_by_id)):
    return article


@router.put(
    "/{article_id}/", response_model=ShowArticle, status_code=status.HTTP_200_OK
)
async def update_article(
    article_update: ArticleUpdate,
    article: Article = Depends(article_by_id),
    user: User = Depends(current_user),
):
    return await _update_article(article=article, article_update=article_update)


@router.delete("/{article_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_article(
    article: Article = Depends(article_by_id), user: User = Depends(current_user)
):
    return await _delete_article(article)
