from typing import TYPE_CHECKING, Optional, Final
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship, attribute_keyed_dict
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.associationproxy import AssociationProxy
from sqlalchemy import ForeignKey, Table, Column, Computed, Index
from sqlalchemy_utils import TSVectorType, LocaleType, CountryType, Country
from babel import Locale
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy import DateTime
from sqlalchemy.sql import func
from uuid import uuid4

from app.db.base_class import Base

if TYPE_CHECKING:
    from app.models.subject import Subject  # noqa: F401
    from app.models.resource import Resource  # noqa: F401
    from app.models.pathway import Pathway  # noqa: F401
    from app.models.node import Node  # noqa: F401

class Theme(Base):
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    created: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    modified: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        server_onupdate=func.now(),
        nullable=False,
    )
    order: Mapped[int] = mapped_column(nullable=False)
    # i18n SEARCH FIELDS
    title: Mapped[dict[str | Locale, "ThemeTitle"]] = relationship(
        collection_class=attribute_keyed_dict("language"),
        cascade="all, delete-orphan",
    )
    description: Mapped[dict[str | Locale, "ThemeDescription"]] = relationship(
        collection_class=attribute_keyed_dict("language"),
        cascade="all, delete-orphan",
    )
    subject: Mapped[set["Subject"]] = relationship(secondary=lambda: theme_subject_table)
    subjects: AssociationProxy[list[str]] = association_proxy("subject", "term")
    # DUBLIN CORE
    country: Mapped[Optional[ARRAY[Country]]] = mapped_column(ARRAY(CountryType), nullable=True)
    spatial: Mapped[Optional[str]] = mapped_column(nullable=True)
    language: Mapped[Locale] = mapped_column(LocaleType, nullable=True)
    # PATHWAY
    resources: Mapped[list["Resource"]] = relationship(
        order_by="Resource.created",
        back_populates="theme",
        cascade="all, delete",
        lazy="dynamic",
    )
    nodes: Mapped[list["Node"]] = relationship(
        order_by="Node.order",
        back_populates="theme",
        cascade="all, delete",
        lazy="dynamic",
    )
    pathway_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("pathway.id", onupdate="CASCADE", ondelete="CASCADE"))
    pathway: Mapped["Pathway"] = relationship(back_populates="themes")


class ThemeTitle(Base):
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    theme_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("theme.id", onupdate="CASCADE", ondelete="CASCADE"))
    title: Mapped[Optional[str]] = mapped_column(index=True)
    language: Mapped[Locale] = mapped_column(LocaleType)
    title_vector: Mapped[TSVectorType] = mapped_column(
        TSVectorType("title", regconfig="pg_catalog.simple"),
        Computed("to_tsvector('pg_catalog.simple', \"title\")", persisted=True),
    )

    __table_args__ = (
        Index("ix_theme_title_vector", title_vector, postgresql_using="gin"),
    )

    def __init__(self, language: str | Locale, title: str):
        self.language = language
        self.title = title


class ThemeDescription(Base):
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    theme_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("theme.id", onupdate="CASCADE", ondelete="CASCADE"))
    description: Mapped[Optional[str]] = mapped_column(index=True)
    language: Mapped[Locale] = mapped_column(LocaleType)
    description_vector: Mapped[TSVectorType] = mapped_column(
        TSVectorType("description", regconfig="pg_catalog.simple"),
        Computed("to_tsvector('pg_catalog.simple', \"description\")", persisted=True),
    )

    __table_args__ = (
        Index("ix_theme_description_vector", description_vector, postgresql_using="gin"),
    )

    def __init__(self, language: str | Locale, description: str):
        self.language = language
        self.description = description


theme_subject_table: Final[Table] = Table(
    "theme_subject",
    Base.metadata,
    Column("theme_id", UUID(as_uuid=True), ForeignKey("theme.id"), primary_key=True),
    Column("subject_id", UUID(as_uuid=True), ForeignKey("subject.id"), primary_key=True),
)
