from datetime import date

from sqlalchemy import select, update, cast, Date
from sqlalchemy.orm import joinedload

from api.article.schemas import ArticleCreate, ArticleUpdate
from database.db_helper import db_helper
from database.models import Article, User


async def _create_article(article_in: ArticleCreate, user_id: int) -> Article:
    async with db_helper.session_factory() as session:
        article = Article(user_id=user_id, **article_in.model_dump())
        session.add(article)
        await session.commit()
        return article


async def _get_articles(
    filter_username: str | None,
    filter_date: date | None,
    skip: int = 0,
    limit: int = 10,
) -> list[Article]:
    async with db_helper.session_factory() as session:
        if filter_date and filter_username:
            query = (
                select(Article)
                .join(User)
                .options(joinedload(Article.user))
                .where(
                    cast(Article.created_at, Date) == cast(filter_date, Date),
                    User.username == filter_username,
                )
                .order_by(Article.id)
                .offset(skip)
                .limit(limit)
            )
            articles = await session.scalars(query)
            return list(articles)
        if filter_username:
            query = (
                select(Article)
                .join(User)
                .options(joinedload(Article.user))
                .where(User.username == filter_username)
                .order_by(Article.id)
                .offset(skip)
                .limit(limit)
            )
            articles = await session.scalars(query)
            return list(articles)
        if filter_date:
            query = (
                select(Article)
                .options(joinedload(Article.user))
                .where(cast(Article.created_at, Date) == cast(filter_date, Date))
                .order_by(Article.id)
                .offset(skip)
                .limit(limit)
            )
            articles = await session.scalars(query)
            return list(articles)
        else:
            query = (
                select(Article)
                .options(joinedload(Article.user))
                .order_by(Article.id)
                .offset(skip)
                .limit(limit)
            )
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
