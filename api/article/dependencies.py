from typing import Annotated

from fastapi import Path, HTTPException, status

from api.article.crud import _get_article_by_id


async def article_by_id(article_id: Annotated[int, Path]):
    article = await _get_article_by_id(article_id=article_id)
    if article is not None:
        return article

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Article {article_id} is not found!",
    )
