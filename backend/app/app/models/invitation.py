from __future__ import annotations
from typing import TYPE_CHECKING, Optional
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UniqueConstraint
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID, ENUM
from sqlalchemy import DateTime
from sqlalchemy.sql import func
from uuid import uuid4

from app.db.base_class import Base
from app.schema_types import InvitationResponseType

if TYPE_CHECKING:
    from app.models.user import User  # noqa: F401
    from app.models.group import Group  # noqa: F401
    from app.models.pathway import Pathway  # noqa: F401


class Invitation(Base):
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    created: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    full_name: Mapped[Optional[str]] = mapped_column(index=True, nullable=True)
    email: Mapped[str] = mapped_column(index=True, nullable=False)
    response: Mapped[ENUM[InvitationResponseType]] = mapped_column(
        ENUM(InvitationResponseType), nullable=False, default=InvitationResponseType.WAITING
    )
    sender_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("user.id", onupdate="CASCADE", ondelete="CASCADE"))
    sender: Mapped["User"] = relationship(back_populates="invitations")
    pathway_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("pathway.id", onupdate="CASCADE", ondelete="CASCADE"))
    pathway: Mapped["Pathway"] = relationship(back_populates="invitations")
    group_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("group.id", onupdate="CASCADE", ondelete="CASCADE"))
    group: Mapped["Group"] = relationship(back_populates="invitations")
    __table_args__ = (UniqueConstraint("email", "pathway_id", "group_id", name="_pathway_invitation_uc"),)
