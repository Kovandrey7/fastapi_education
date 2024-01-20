from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, status, Query

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
    ShowArticleAfterCreate,
    ShowArticleAfterUpdate,
)
from authentication.auth import get_current_user
from database.models import User, Article

router = APIRouter(tags=["Article"], prefix="/article")


@router.post(
    "/", response_model=ShowArticleAfterCreate, status_code=status.HTTP_201_CREATED
)
async def create_article(
    article_in: ArticleCreate, user: User = Depends(get_current_user)
) -> ShowArticleAfterCreate:
    new_article = await _create_article(article_in=article_in, user_id=user.id)
    return ShowArticleAfterCreate(
        title=new_article.title,
        content=new_article.content,
        id=new_article.id,
        created_at=new_article.created_at,
        user_id=new_article.user_id,
    )


@router.get("/", response_model=list[ShowArticle], status_code=status.HTTP_200_OK)
async def get_articles(
    page: int = 1,
    limit: int = 5,
    filter_username: Annotated[str | None, Query(alias="username")] = None,
    filter_date: Annotated[
        date | None, Query(alias="date", description="Format 2024-01-21")
    ] = None,
) -> list[ShowArticle]:
    articles = await _get_articles(
        page=page, limit=limit, filter_username=filter_username, filter_date=filter_date
    )
    return [
        ShowArticle(
            id=article.id,
            title=article.title,
            content=article.content,
            created_at=article.created_at,
            user_id=article.user_id,
            username=article.user.username,
        )
        for article in articles
    ]


@router.get(
    "/{article_id}/", response_model=ShowArticle, status_code=status.HTTP_200_OK
)
async def get_article_by_id(article: Article = Depends(article_by_id)) -> ShowArticle:
    return ShowArticle(
        id=article.id,
        title=article.title,
        content=article.content,
        created_at=article.created_at,
        user_id=article.user_id,
        username=article.user.username,
    )


@router.put(
    "/{article_id}/",
    response_model=ShowArticleAfterUpdate,
    status_code=status.HTTP_200_OK,
)
async def update_article(
    article_update: ArticleUpdate,
    article: Article = Depends(article_by_id),
    user: User = Depends(get_current_user),
) -> ShowArticleAfterUpdate:
    article_update = await _update_article(
        article=article, article_update=article_update
    )
    return ShowArticleAfterUpdate(
        id=article_update.id,
        title=article_update.title,
        content=article_update.content,
        created_at=article_update.created_at,
        user_id=article_update.user_id,
    )


@router.delete("/{article_id}/", status_code=status.HTTP_200_OK)
async def delete_article(
    article: Article = Depends(article_by_id), user: User = Depends(get_current_user)
) -> dict:
    await _delete_article(article)
    return {"details": f"Article with id:{article.id} deleted successfully"}
