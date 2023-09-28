from __future__ import annotations
from typing import TYPE_CHECKING, Optional, Final
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.associationproxy import AssociationProxy
from sqlalchemy import ForeignKey, DateTime, Table, Column, Computed, Index
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_utils import TSVectorType, LocaleType, CountryType, Country
from babel import Locale
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from uuid import uuid4

from app.db.base_class import Base
from app.schema_types.pathway import PathwayType
from app.models.pathway import Pathway
from app.models.response import Response

if TYPE_CHECKING:
    from app.models.token import Token  # noqa: F401
    from app.models.subject import Subject  # noqa: F401
    from app.models.invitation import Invitation  # noqa: F401
    from app.models.role import Role  # noqa: F401
    from app.models.comment import Comment  # noqa: F401


class User(Base):
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    created: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    modified: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        server_onupdate=func.now(),
        nullable=False,
    )
    # METADATA
    full_name: Mapped[str] = mapped_column(index=True, nullable=True)
    email: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    hashed_password: Mapped[Optional[str]] = mapped_column(nullable=True)
    description: Mapped[Optional[str]] = mapped_column(index=True)
    description_vector: Mapped[TSVectorType] = mapped_column(
        TSVectorType("description", regconfig="pg_catalog.simple"),
        Computed("to_tsvector('pg_catalog.simple', \"description\")", persisted=True),
    )
    subject: Mapped[set["Subject"]] = relationship(secondary=lambda: user_subject_table)
    subjects: AssociationProxy[list[str]] = association_proxy("subject", "term")
    country: Mapped[Optional[list[Country]]] = mapped_column(ARRAY(CountryType), nullable=True)
    spatial: Mapped[Optional[str]] = mapped_column(nullable=True)
    language: Mapped[Locale] = mapped_column(LocaleType, nullable=True)
    # AUTHENTICATION AND PERSISTENCE
    totp_secret: Mapped[Optional[str]] = mapped_column(nullable=True)
    totp_counter: Mapped[Optional[int]] = mapped_column(nullable=True)
    email_validated: Mapped[bool] = mapped_column(default=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    refresh_tokens: Mapped[list["Token"]] = relationship(
        foreign_keys="[Token.authenticates_id]", cascade="all, delete", back_populates="authenticates", lazy="dynamic"
    )
    # PATHWAY AND RESPONSIBILITIES
    roles: Mapped[list["Role"]] = relationship(back_populates="researcher", cascade="all, delete", lazy="dynamic")
    invitations: Mapped[list["Invitation"]] = relationship(
        back_populates="sender", cascade="all, delete", lazy="dynamic"
    )
    # ANSWERS
    responses: Mapped[list["Response"]] = relationship(
        order_by="Response.created", back_populates="respondent", cascade="all, delete", lazy="dynamic"
    )
    comments: Mapped[list["Comment"]] = relationship(
        order_by="Comment.created", back_populates="researcher", cascade="all, delete", lazy="dynamic"
    )

    # Query-based hybrid properties
    @hybrid_property
    def completedPersonalPathway(self) -> bool:
        last_response = self.responses.filter(
            Pathway.pathType == PathwayType.PERSONAL
        ).order_by(None).order_by(Response.created.desc()).first()
        if not last_response or last_response.node.after.first():
            # Either they've not filled in, or the response isn't for the last node
            return False
        return True

    __table_args__ = (
        Index("ix_user_description_vector", description_vector, postgresql_using="gin"),
    )

user_subject_table: Final[Table] = Table(
    "user_subject",
    Base.metadata,
    Column("user_id", UUID(as_uuid=True), ForeignKey("user.id"), primary_key=True),
    Column("subject_id", UUID(as_uuid=True), ForeignKey("subject.id"), primary_key=True),
)
