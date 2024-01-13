from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Integer, String, func, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.models.base import Base

if TYPE_CHECKING:
    from .user import User


class Article(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    content: Mapped[str] = mapped_column(Text, default="", server_default="")
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), default=datetime.utcnow
    )
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("user.id", ondelete="CASCADE")
    )

    user: Mapped["User"] = relationship(back_populates="articles")
