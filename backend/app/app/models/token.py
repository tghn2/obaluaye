from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401


class Token(Base):
    token: Mapped[str] = mapped_column(primary_key=True, index=True)
    authenticates_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.id", onupdate="CASCADE", ondelete="CASCADE")
    )
    authenticates: Mapped["User"] = relationship(back_populates="refresh_tokens")
