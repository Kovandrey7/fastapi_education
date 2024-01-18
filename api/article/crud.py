from datetime import date

from sqlalchemy import select, update
from sqlalchemy.orm import joinedload

from api.article.filter_query import (
    query_filter_date_and_username,
    query_filter_username,
    query_filter_date,
    query_without_filters,
)
from api.article.schemas import ArticleCreate, ArticleUpdate
from database.db_helper import db_helper
from database.models import Article


async def _create_article(article_in: ArticleCreate, user_id: int) -> Article:
    async with db_helper.session_factory() as session:
        article = Article(user_id=user_id, **article_in.model_dump())
        session.add(article)
        await session.commit()
        return article


async def _get_articles(
    filter_username: str | None,
    filter_date: date | None,
    page: int,
    limit: int,
) -> list[Article]:
    async with db_helper.session_factory() as session:
        if filter_date and filter_username:
            query = query_filter_date_and_username(
                filter_username, filter_date, page, limit
            )
            articles = await session.scalars(query)
            return list(articles)
        if filter_username:
            query = query_filter_username(filter_username, page, limit)
            articles = await session.scalars(query)
            return list(articles)
        if filter_date:
            query = query_filter_date(filter_date, page, limit)
            articles = await session.scalars(query)
            return list(articles)
        else:
            query = query_without_filters(page, limit)
            articles = await session.scalars(query)
            return list(articles)


async def _get_article_by_id(article_id: int) -> Article | None:
    async with db_helper.session_factory() as session:
        query = (
            select(Article)
            .options(joinedload(Article.user))
            .where(Article.id == article_id)
        )
        article = await session.scalar(query)
        return article


async def _update_article(
    article: Article,
    article_update: ArticleUpdate,
) -> Article:
    async with db_helper.session_factory() as session:
        stmt = (
            update(Article)
            .where(Article.id == article.id)
            .values(article_update.model_dump(exclude_none=True))
            .returning(Article)
        )
        article_update = await session.scalar(stmt)
        await session.commit()
        return article_update


async def _delete_article(article: Article) -> None:
    async with db_helper.session_factory() as session:
        await session.delete(article)
        await session.commit()
