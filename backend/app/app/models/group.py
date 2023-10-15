from __future__ import annotations
from typing import TYPE_CHECKING, Optional, Final
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.associationproxy import AssociationProxy
from sqlalchemy import ForeignKey, DateTime, Table, Column, Computed, Index
from sqlalchemy_utils import TSVectorType, LocaleType, CountryType, Country
from babel import Locale
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from uuid import uuid4

from app.db.base_class import Base

if TYPE_CHECKING:
    from app.models.subject import Subject  # noqa: F401
    from app.models.role import Role  # noqa: F401
    from app.models.invitation import Invitation  # noqa: F401
    from app.models.response import Response  # noqa: F401


class Group(Base):
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    created: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    modified: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        server_onupdate=func.now(),
        nullable=False,
    )
    isActive: Mapped[bool] = mapped_column(default=True)
    isComplete: Mapped[bool] = mapped_column(default=False)
    # METADATA
    title: Mapped[str] = mapped_column(index=True, nullable=True)
    title_vector: Mapped[TSVectorType] = mapped_column(
        TSVectorType("title", regconfig="pg_catalog.simple"),
        Computed("to_tsvector('pg_catalog.simple', \"title\")", persisted=True),
    )
    description: Mapped[Optional[str]] = mapped_column(index=True)
    description_vector: Mapped[TSVectorType] = mapped_column(
        TSVectorType("description", regconfig="pg_catalog.simple"),
        Computed("to_tsvector('pg_catalog.simple', \"description\")", persisted=True),
    )
    subject: Mapped[set["Subject"]] = relationship(secondary=lambda: group_subject_table)
    subjects: AssociationProxy[list[str]] = association_proxy("subject", "term")
    country: Mapped[Optional[list[Country]]] = mapped_column(ARRAY(CountryType), nullable=True)
    spatial: Mapped[Optional[str]] = mapped_column(nullable=True)
    language: Mapped[Locale] = mapped_column(LocaleType, nullable=True)
    # MEMBERS AND PATHWAY
    roles: Mapped[list["Role"]] = relationship(back_populates="group", cascade="all, delete", lazy="dynamic")
    invitations: Mapped[list["Invitation"]] = relationship(
        back_populates="group", cascade="all, delete", lazy="dynamic"
    )
    # ANSWERS
    responses: Mapped[list["Response"]] = relationship(
        back_populates="group", cascade="all, delete", lazy="dynamic"
    )

    __table_args__ = (
        Index("ix_group_title_vector", title_vector, postgresql_using="gin"),
        Index("ix_group_description_vector", description_vector, postgresql_using="gin"),
    )

group_subject_table: Final[Table] = Table(
    "group_subject",
    Base.metadata,
    Column("group_id", UUID(as_uuid=True), ForeignKey("group.id"), primary_key=True),
    Column("subject_id", UUID(as_uuid=True), ForeignKey("subject.id"), primary_key=True),
)
