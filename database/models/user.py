from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import Integer, String, Boolean
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.models.base import Base

if TYPE_CHECKING:
    from .article import Article


class Role(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"
    SUPERADMIN = "SUPERADMIN"


class User(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str]
    email: Mapped[str] = mapped_column(String, unique=True)
    role: Mapped[list[str]] = mapped_column(ARRAY(String), default=[Role.USER])
    hashed_password: Mapped[str] = mapped_column(String(length=1024))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    articles: Mapped[list["Article"]] = relationship(back_populates="user")

    @property
    def is_superadmin(self) -> bool:
        return Role.SUPERADMIN in self.role

    @property
    def is_admin(self) -> bool:
        return Role.ADMIN in self.role

    def enrich_admin_roles_by_admin_role(self):
        if not self.is_admin:
            return list({*self.role, Role.ADMIN})

    def remove_admin_privileges_from_model(self):
        if self.is_admin:
            return list({role for role in self.role if role != Role.ADMIN})
