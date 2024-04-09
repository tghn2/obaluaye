from typing import TYPE_CHECKING, Optional
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship, attribute_keyed_dict
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


class CollectionSelection(Base):
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    created: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    modified: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        server_onupdate=func.now(),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(index=True, nullable=False)
    # COLLECTED SELECTION TERMS
    language: Mapped[Locale] = mapped_column(LocaleType, nullable=True)
    title: Mapped[dict[str | Locale, "CollectionSelectionTitle"]] = relationship(
        collection_class=attribute_keyed_dict("language"),
        cascade="all, delete-orphan",
    )
    isMulti: Mapped[bool] = mapped_column(default=False)
    selection: Mapped[list["Selection"]] = relationship(
        back_populates="collection",
        cascade="all, delete",
        lazy="dynamic",
    )


class CollectionSelectionTitle(Base):
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    collection_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("collectionselection.id", onupdate="CASCADE", ondelete="CASCADE")
    )
    collection: Mapped["CollectionSelection"] = relationship(back_populates="title")
    title: Mapped[Optional[str]] = mapped_column(index=True)
    language: Mapped[Locale] = mapped_column(LocaleType)

    def __init__(self, language: str | Locale, title: str, back_ref: CollectionSelection | None = None):
        self.language = language
        self.title = title
        if back_ref:
            self.collection = back_ref


class Selection(Base):
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    created: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    modified: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        server_onupdate=func.now(),
        nullable=False,
    )
    # SELECTION TERM
    language: Mapped[Locale] = mapped_column(LocaleType, nullable=True)
    term: Mapped[dict[str | Locale, "SelectionTerm"]] = relationship(
        collection_class=attribute_keyed_dict("language"),
        cascade="all, delete-orphan",
    )
    # RELATIONSHIPS
    collection_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("collectionselection.id"), nullable=True)
    collection: Mapped["CollectionSelection"] = relationship(back_populates="selection", foreign_keys=[collection_id])
    researchers: Mapped[list["User"]] = relationship(
        secondary="user_selection",
        back_populates="selection",
        lazy="dynamic",
    )


class SelectionTerm(Base):
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    selection_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("selection.id", onupdate="CASCADE", ondelete="CASCADE")
    )
    selection: Mapped["Selection"] = relationship(back_populates="term")
    term: Mapped[Optional[str]] = mapped_column(index=True)
    language: Mapped[Locale] = mapped_column(LocaleType)

    def __init__(self, language: str | Locale, term: str, back_ref: Selection | None = None):
        self.language = language
        self.term = term
        if back_ref:
            self.selection = back_ref
