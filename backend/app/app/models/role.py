from __future__ import annotations
from typing import TYPE_CHECKING
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID, ENUM
from sqlalchemy import DateTime
from sqlalchemy.sql import func
from uuid import uuid4

from app.db.base_class import Base
from app.schema_types import RoleType

if TYPE_CHECKING:
    from app.models.user import User  # noqa: F401
    from app.models.group import Group  # noqa: F401
    from app.models.pathway import Pathway  # noqa: F401

class Role(Base):
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    created: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    # WHO
    researcher_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.id", onupdate="CASCADE", ondelete="CASCADE")
    )
    researcher: Mapped["User"] = relationship(
        back_populates="roles", foreign_keys=[researcher_id], order_by="User.email"
    )
    group_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("group.id"))
    group: Mapped["Group"] = relationship(
        back_populates="roles", foreign_keys=[group_id]  # , order_by="Group.title"
    )
    # HAS RESPONSIBILITY
    responsibility: Mapped[ENUM[RoleType]] = mapped_column(ENUM(RoleType), nullable=False, default=RoleType.VIEWER)
    # FOR
    pathway_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("pathway.id", onupdate="CASCADE", ondelete="CASCADE")
    )
    pathway: Mapped["Pathway"] = relationship(back_populates="authorisations", foreign_keys=[pathway_id])
