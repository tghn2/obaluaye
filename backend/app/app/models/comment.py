from typing import TYPE_CHECKING
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from sqlalchemy_utils import LocaleType
from babel import Locale
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import DateTime
from sqlalchemy.sql import func
from uuid import uuid4

from app.db.base_class import Base

if TYPE_CHECKING:
    from app.models.user import User  # noqa: F401
    from app.models.response import Response  # noqa: F401

class Comment(Base):
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    created: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    modified: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        server_onupdate=func.now(),
        nullable=False,
    )
    # COMMENT
    resolved: Mapped[bool] = mapped_column(default=False)
    language: Mapped[Locale] = mapped_column(LocaleType, nullable=True)
    content: Mapped[str]
    researcher_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("user.id"))
    researcher: Mapped["User"] = relationship(
        back_populates="comments", foreign_keys=[researcher_id], order_by="User.email"
    )
    response_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("response.id", onupdate="CASCADE", ondelete="CASCADE"))
    response: Mapped["Response"] = relationship(back_populates="comments")
