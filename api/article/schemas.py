from pydantic import BaseModel, ConfigDict


class ArticleBase(BaseModel):
    title: str
    content: str


class ArticleCreate(ArticleBase):
    pass


class ArticleUpdate(ArticleBase):
    title: str | None = None
    content: str | None = None


class ShowArticle(ArticleBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
