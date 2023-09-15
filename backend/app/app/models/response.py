from typing import TYPE_CHECKING
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from sqlalchemy_utils import LocaleType
from babel import Locale
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy import DateTime
from sqlalchemy.sql import func
from uuid import uuid4
import json

from app.db.base_class import Base

if TYPE_CHECKING:
    from app.models.user import User  # noqa: F401
    from app.models.group import Group  # noqa: F401
    from app.models.comment import Comment  # noqa: F401
    from app.models.node import Node  # noqa: F401

class Response(Base):
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    created: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    modified: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        server_onupdate=func.now(),
        nullable=False,
    )
    # RESPONSE
    language: Mapped[Locale] = mapped_column(LocaleType, nullable=True)
    answer: Mapped[json] = mapped_column(JSONB)
    # ANSWERS
    node_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("node.id", onupdate="CASCADE", ondelete="CASCADE")
    )
    node: Mapped["Node"] = relationship(back_populates="responses")
    respondent_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("user.id"))
    respondent: Mapped["User"] = relationship(back_populates="responses")
    group_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("group.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=True
    )
    group: Mapped["Group"] = relationship(back_populates="responses")
    # COMMENTS
    comments: Mapped[list["Comment"]] = relationship(
        order_by="Comment.created",
        back_populates="response",
        cascade="all, delete",
        lazy="dynamic"
    )
