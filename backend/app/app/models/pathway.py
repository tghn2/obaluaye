from typing import TYPE_CHECKING, Optional, Final
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship, attribute_keyed_dict
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.associationproxy import AssociationProxy
from sqlalchemy import ForeignKey, Table, Column, Computed, Index
from sqlalchemy_utils import TSVectorType, LocaleType, CountryType, Country
from babel import Locale
from sqlalchemy.dialects.postgresql import UUID, ENUM, ARRAY
from sqlalchemy import DateTime
from sqlalchemy.sql import func
from uuid import uuid4

from app.db.base_class import Base
from app.schema_types.pathway import PathwayType

if TYPE_CHECKING:
    from app.models.subject import Subject  # noqa: F401
    from app.models.resource import Resource  # noqa: F401
    from app.models.theme import Theme  # noqa: F401
    from app.models.invitation import Invitation  # noqa: F401
    from app.models.role import Role  # noqa: F401
    from app.models.node import Node  # noqa: F401

class Pathway(Base):
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    created: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    modified: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        server_onupdate=func.now(),
        nullable=False,
    )
    isPrivate: Mapped[bool] = mapped_column(default=False)
    isProtected: Mapped[bool] = mapped_column(default=False)
    pathType: Mapped[ENUM[PathwayType]] = mapped_column(ENUM(PathwayType), nullable=False, default=PathwayType.RESEARCH)
    # i18n SEARCH FIELDS
    title: Mapped[dict[str | Locale, "PathwayTitle"]] = relationship(
        collection_class=attribute_keyed_dict("language"),
        cascade="all, delete-orphan",
    )
    description: Mapped[dict[str | Locale, "PathwayDescription"]] = relationship(
        collection_class=attribute_keyed_dict("language"),
        cascade="all, delete-orphan",
    )
    subject: Mapped[set["Subject"]] = relationship(secondary=lambda: pathway_subject_table)
    subjects: AssociationProxy[list[str]] = association_proxy("subject", "term")
    # DUBLIN CORE
    country: Mapped[Optional[list[Country]]] = mapped_column(ARRAY(CountryType), nullable=True)
    spatial: Mapped[Optional[str]] = mapped_column(nullable=True)
    temporalStart: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    temporalEnd: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    language: Mapped[Locale] = mapped_column(LocaleType, nullable=True)
    bibliographicCitation: Mapped[Optional[str]] = mapped_column(nullable=True)
    # MEMBERS AND MEMBERSHIP MANAGEMENT
    invitations: Mapped[list["Invitation"]] = relationship(
        back_populates="pathway", cascade="all, delete", lazy="dynamic"
    )
    authorisations: Mapped[list["Role"]] = relationship(
        back_populates="pathway", cascade="all, delete", lazy="dynamic"
    )
    # PATHWAY
    resources: Mapped[list["Resource"]] = relationship(
        order_by="Resource.created",
        back_populates="pathway",
        cascade="all, delete",
        lazy="dynamic",
    )
    themes: Mapped[list["Theme"]] = relationship(
        order_by="Theme.order",
        back_populates="pathway",
        cascade="all, delete",
        lazy="dynamic",
    )
    nodes: Mapped[list["Node"]] = relationship(
        order_by="Node.order",
        back_populates="pathway",
        cascade="all, delete",
        lazy="dynamic",
    )


class PathwayTitle(Base):
    # A combination of Dictionary Collection and TSVector searchable term
    # https://docs.sqlalchemy.org/en/20/orm/collection_api.html#dictionary-collections
    # https://sqlalchemy-utils.readthedocs.io/en/latest/data_types.html#module-sqlalchemy_utils.types.locale
    # https://sqlalchemy-utils.readthedocs.io/en/latest/data_types.html#module-sqlalchemy_utils.types.ts_vector
    # Access this term using:
    #       pathway.title[locale]
    # Where `locale` is a Babel type.
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    pathway_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("pathway.id", onupdate="CASCADE", ondelete="CASCADE"))
    pathway: Mapped["Pathway"] = relationship(back_populates="title")
    title: Mapped[Optional[str]] = mapped_column(index=True)
    language: Mapped[Locale] = mapped_column(LocaleType)
    title_vector: Mapped[TSVectorType] = mapped_column(
        TSVectorType("title", regconfig="pg_catalog.simple"),
        Computed("to_tsvector('pg_catalog.simple', \"title\")", persisted=True),
    )

    __table_args__ = (
        # Indexing the TSVector column
        Index("ix_pathway_title_vector", title_vector, postgresql_using="gin"),
    )

    def __init__(self, language: str | Locale, title: str, back_ref: Pathway | None = None):
        self.language = language
        self.title = title
        if back_ref:
            self.pathway = back_ref


class PathwayDescription(Base):
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    pathway_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("pathway.id", onupdate="CASCADE", ondelete="CASCADE"))
    pathway: Mapped["Pathway"] = relationship(back_populates="description")
    description: Mapped[Optional[str]] = mapped_column(index=True)
    language: Mapped[Locale] = mapped_column(LocaleType)
    description_vector: Mapped[TSVectorType] = mapped_column(
        TSVectorType("description", regconfig="pg_catalog.simple"),
        Computed("to_tsvector('pg_catalog.simple', \"description\")", persisted=True),
    )

    __table_args__ = (
        Index("ix_pathway_description_vector", description_vector, postgresql_using="gin"),
    )

    def __init__(self, language: str | Locale, description: str, back_ref: Pathway | None = None):
        self.language = language
        self.description = description
        if back_ref:
            self.pathway = back_ref


pathway_subject_table: Final[Table] = Table(
    "pathway_subject",
    Base.metadata,
    Column("pathway_id", UUID(as_uuid=True), ForeignKey("pathway.id"), primary_key=True),
    Column("subject_id", UUID(as_uuid=True), ForeignKey("subject.id"), primary_key=True),
)
