from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ArticleBase(BaseModel):
    title: str
    content: str


class ArticleCreate(ArticleBase):
    pass


class ShowArticleAfterCreate(ArticleBase):
    id: int
    created_at: datetime
    user_id: int


class ArticleUpdate(ArticleBase):
    title: str | None = None
    content: str | None = None


class ShowArticleAfterUpdate(ArticleBase):
    id: int
    created_at: datetime
    user_id: int


class ShowArticle(ArticleBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    user_id: int
    username: str
