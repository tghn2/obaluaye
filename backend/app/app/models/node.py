from typing import TYPE_CHECKING, Optional, Final
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship, attribute_keyed_dict
from sqlalchemy import ForeignKey, Table, Column
from sqlalchemy_utils import LocaleType
from babel import Locale
from sqlalchemy.dialects.postgresql import UUID, ENUM, JSONB
from sqlalchemy import DateTime
from sqlalchemy.sql import func
from uuid import uuid4
import json

from app.db.base_class import Base
from app.schema_types.node import NodeType

if TYPE_CHECKING:
    from app.models.subject import Subject  # noqa: F401
    from app.models.resource import Resource  # noqa: F401
    from app.models.pathway import Pathway  # noqa: F401
    from app.models.theme import Theme  # noqa: F401
    from app.models.response import Response  # noqa: F401

class Node(Base):
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    created: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    modified: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        server_onupdate=func.now(),
        nullable=False,
    )
    # NODE PATHWAY
    order: Mapped[int] = mapped_column(nullable=False)
    formType: Mapped[ENUM[NodeType]] = mapped_column(ENUM(NodeType), nullable=False)
    language: Mapped[Locale] = mapped_column(LocaleType, nullable=True)
    after: Mapped[list["Node"]] = relationship(
        secondary="pathway_sequence",
        primaryjoin="Node.id == pathway_sequence.c.before_id",
        secondaryjoin="Node.id == pathway_sequence.c.after_id",
        back_populates="before",
        lazy="dynamic",
    )
    before: Mapped[list["Node"]] = relationship(
        secondary="pathway_sequence",
        primaryjoin="Node.id == pathway_sequence.c.after_id",
        secondaryjoin="Node.id == pathway_sequence.c.before_id",
        back_populates="after",
        lazy="dynamic",
    )
    # FORM
    question: Mapped[dict[str | Locale, "NodeQuestion"]] = relationship(
        collection_class=attribute_keyed_dict("language"),
        cascade="all, delete-orphan",
    )
    form: Mapped[dict[str | Locale, "NodeForm"]] = relationship(
        collection_class=attribute_keyed_dict("language"),
        cascade="all, delete-orphan",
    )
    # PATHWAY
    resources: Mapped[list["Resource"]] = relationship(
        order_by="Resource.created",
        back_populates="node",
        cascade="all, delete",
        lazy="dynamic",
    )
    pathway_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("pathway.id", onupdate="CASCADE", ondelete="CASCADE"))
    pathway: Mapped["Pathway"] = relationship(back_populates="nodes")
    theme_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("theme.id"), nullable=True)
    theme: Mapped["Theme"] = relationship(back_populates="nodes")
    responses: Mapped[list["Response"]] = relationship(
        back_populates="node", cascade="all, delete", lazy="dynamic"
    )


# For self-referential many-to-many relationship
# https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#setting-bi-directional-many-to-many
# https://medium.com/@mandyranero/how-to-implement-and-use-a-flask-sqlalchemy-self-referential-many-to-many-relationship-11aa0179e13a
# https://stackoverflow.com/questions/73447328/self-referencing-many-to-many-relationship-with-extra-column-in-association-obje
# https://stackoverflow.com/questions/66424424/self-referencing-many-to-many-relationship-with-an-association-object-in-sqlalch
pathway_sequence_table: Final[Table] = Table(
    "pathway_sequence",
    Base.metadata,
    Column("before_id", UUID(as_uuid=True), ForeignKey("node.id"), primary_key=True),
    Column("after_id", UUID(as_uuid=True), ForeignKey("node.id"), primary_key=True),
)


class NodeQuestion(Base):
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    node_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("node.id", onupdate="CASCADE", ondelete="CASCADE"))
    question: Mapped[Optional[str]] = mapped_column(index=True)
    language: Mapped[Locale] = mapped_column(LocaleType)

    def __init__(self, language: str | Locale, question: str):
        self.language = language
        self.question = question


class NodeForm(Base):
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    node_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("node.id", onupdate="CASCADE", ondelete="CASCADE"))
    # Pay attention to JSON field mutability
    # https://amercader.net/blog/beware-of-json-fields-in-sqlalchemy/
    # For these small data fields, create a copy of the JSON field dict before making the changes
    # Depending on the size of your objects and the frequency of updates this approach might be sufficent
    # Alternatively: https://github.com/edelooff/sqlalchemy-json
    # https://docs.sqlalchemy.org/en/20/core/custom_types.html#marshal-json-strings'
    # https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.JSON
    form: Mapped[json] = mapped_column(JSONB)
    language: Mapped[Locale] = mapped_column(LocaleType)

    def __init__(self, language: str | Locale, form: str):
        self.language = language
        self.form = form
