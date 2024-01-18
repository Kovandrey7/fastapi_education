from datetime import date

from sqlalchemy import select, cast, Date, Select
from sqlalchemy.orm import joinedload

from database.models import Article, User


def query_filter_date_and_username(
    filter_username: str | None, filter_date: date | None, page: int, limit: int
) -> Select:
    query = (
        select(Article)
        .join(User)
        .options(joinedload(Article.user))
        .where(
            cast(Article.created_at, Date) == cast(filter_date, Date),
            User.username == filter_username,
        )
        .order_by(Article.id)
        .offset((page - 1) * limit)
        .limit(limit)
    )
    return query


def query_filter_username(filter_username: str | None, page: int, limit: int) -> Select:
    query = (
        select(Article)
        .join(User)
        .options(joinedload(Article.user))
        .where(User.username == filter_username)
        .order_by(Article.id)
        .offset((page - 1) * limit)
        .limit(limit)
    )
    return query


def query_filter_date(filter_date: date | None, page: int, limit: int) -> Select:
    query = (
        select(Article)
        .options(joinedload(Article.user))
        .where(cast(Article.created_at, Date) == cast(filter_date, Date))
        .order_by(Article.id)
        .offset((page - 1) * limit)
        .limit(limit)
    )
    return query


def query_without_filters(page: int, limit: int) -> Select:
    query = (
        select(Article)
        .options(joinedload(Article.user))
        .order_by(Article.id)
        .offset((page - 1) * limit)
        .limit(limit)
    )
    return query
