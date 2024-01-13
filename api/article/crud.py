from sqlalchemy import select, update

from api.article.schemas import ArticleCreate, ArticleUpdate
from database.db_helper import db_helper
from database.models import Article


async def _create_article(article_in: ArticleCreate, user_id: int) -> Article:
    async with db_helper.session_factory() as session:
        article = Article(user_id=user_id, **article_in.model_dump())
        session.add(article)
        await session.commit()
        return article


async def _get_articles() -> list[Article]:
    async with db_helper.session_factory() as session:
        query = select(Article).order_by(Article.id)
        result = await session.execute(query)
        articles = result.scalars().all()
        return list(articles)


async def _get_article_by_id(article_id: int) -> Article | None:
    async with db_helper.session_factory() as session:
        return await session.get(Article, article_id)


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
        await session.execute(stmt)
        await session.commit()
        return article


async def _delete_article(article: Article) -> None:
    async with db_helper.session_factory() as session:
        await session.delete(article)
        await session.commit()
