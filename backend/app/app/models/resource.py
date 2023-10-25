from typing import TYPE_CHECKING, Optional
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship, attribute_keyed_dict
from sqlalchemy import ForeignKey, Computed, Index
from sqlalchemy_utils import TSVectorType, LocaleType
from babel import Locale
from sqlalchemy.dialects.postgresql import UUID, ENUM
from sqlalchemy import DateTime
from sqlalchemy.sql import func
from uuid import uuid4

from app.db.base_class import Base
from app.schema_types.resource import ResourceType

if TYPE_CHECKING:
    from app.models.subject import Subject  # noqa: F401
    from app.models.pathway import Pathway  # noqa: F401
    from app.models.theme import Theme  # noqa: F401
    from app.models.node import Node  # noqa: F401

class Resource(Base):
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    created: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    modified: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        server_onupdate=func.now(),
        nullable=False,
    )
    resourceType: Mapped[ENUM[ResourceType]] = mapped_column(ENUM(ResourceType), nullable=False)
    # i18n SEARCH FIELDS
    title: Mapped[dict[str | Locale, "ResourceTitle"]] = relationship(
        collection_class=attribute_keyed_dict("language"),
        cascade="all, delete-orphan",
    )
    description: Mapped[dict[str | Locale, "ResourceDescription"]] = relationship(
        collection_class=attribute_keyed_dict("language"),
        cascade="all, delete-orphan",
    )
    # RESOURCE
    content: Mapped[dict[str | Locale, "ResourceContent"]] = relationship(
        collection_class=attribute_keyed_dict("language"),
        cascade="all, delete-orphan",
    )
    language: Mapped[Locale] = mapped_column(LocaleType, nullable=True)
    # PATHWAY
    pathway_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("pathway.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=True
    )
    pathway: Mapped["Pathway"] = relationship(back_populates="resources")
    theme_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("theme.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=True
    )
    theme: Mapped["Theme"] = relationship(back_populates="resources")
    node_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("node.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=True
    )
    node: Mapped["Node"] = relationship(back_populates="resources")


class ResourceTitle(Base):
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    resource_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("resource.id", onupdate="CASCADE", ondelete="CASCADE"))
    resource: Mapped["Resource"] = relationship(back_populates="title")
    title: Mapped[Optional[str]] = mapped_column(index=True)
    language: Mapped[Locale] = mapped_column(LocaleType)
    # title_vector: Mapped[TSVectorType] = mapped_column(
    #     TSVectorType("title", regconfig="pg_catalog.simple"),
    #     Computed("to_tsvector('pg_catalog.simple', \"title\")", persisted=True),
    #     nullable=True,
    # )

    # __table_args__ = (
    #     Index("ix_resource_title_vector", title_vector, postgresql_using="gin"),
    # )

    def __init__(self, language: str | Locale, title: str, back_ref: Resource | None = None):
        self.language = language
        self.title = title
        if back_ref:
            self.resource = back_ref


class ResourceDescription(Base):
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    resource_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("resource.id", onupdate="CASCADE", ondelete="CASCADE"))
    resource: Mapped["Resource"] = relationship(back_populates="description")
    description: Mapped[Optional[str]] = mapped_column(index=True)
    language: Mapped[Locale] = mapped_column(LocaleType)
    # description_vector: Mapped[TSVectorType] = mapped_column(
    #     TSVectorType("description", regconfig="pg_catalog.simple"),
    #     Computed("to_tsvector('pg_catalog.simple', \"description\")", persisted=True),
    #     nullable=True,
    # )

    # __table_args__ = (
    #     Index("ix_resource_description_vector", description_vector, postgresql_using="gin"),
    # )

    def __init__(self, language: str | Locale, description: str, back_ref: Resource | None = None):
        self.language = language
        self.description = description
        if back_ref:
            self.resource = back_ref


class ResourceContent(Base):
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    resource_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("resource.id", onupdate="CASCADE", ondelete="CASCADE"))
    resource: Mapped["Resource"] = relationship(back_populates="content")
    content: Mapped[Optional[str]]
    language: Mapped[Locale] = mapped_column(LocaleType)

    def __init__(self, language: str | Locale, content: str, back_ref: Resource | None = None):
        self.language = language
        self.content = content
        if back_ref:
            self.resource = back_ref
