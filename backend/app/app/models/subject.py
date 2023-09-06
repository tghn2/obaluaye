from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Computed, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy_utils import TSVectorType
from uuid import uuid4

from app.db.base_class import Base


class Subject(Base):
    # Sort of but not quite: https://docs.sqlalchemy.org/en/20/_modules/examples/graphs/directed_graph.html
    # https://docs.sqlalchemy.org/en/20/orm/extensions/associationproxy.html
    # Subjects aren't language-specific, so these can be used irrespective of language - one pool for everything
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    term: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    term_vector: Mapped[TSVectorType] = mapped_column(
        TSVectorType("term", regconfig="pg_catalog.simple"),
        Computed("to_tsvector('pg_catalog.simple', \"term\")", persisted=True),
    )

    __table_args__ = (
        # Indexing the TSVector column
        Index("ix_subject_term_vector", term_vector, postgresql_using="gin"),
    )

    def __init__(self, term: str):
        self.term = term
