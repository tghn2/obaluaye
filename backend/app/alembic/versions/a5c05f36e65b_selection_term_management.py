"""Selection term management

Revision ID: a5c05f36e65b
Revises: 78810d57a727
Create Date: 2024-04-09 07:36:02.489501

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy_utils import LocaleType


# revision identifiers, used by Alembic.
revision = "a5c05f36e65b"
down_revision = "78810d57a727"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "collectionselection",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("modified", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("language", LocaleType(), nullable=True),
        sa.Column("isMulti", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_collectionselection_id"), "collectionselection", ["id"], unique=False)
    op.create_index(op.f("ix_collectionselection_name"), "collectionselection", ["name"], unique=False)
    op.create_table(
        "collectionselectiontitle",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("collection_id", sa.UUID(), nullable=False),
        sa.Column("title", sa.String(), nullable=True),
        sa.Column("language", LocaleType(), nullable=False),
        sa.ForeignKeyConstraint(["collection_id"], ["collectionselection.id"], onupdate="CASCADE", ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_collectionselectiontitle_id"), "collectionselectiontitle", ["id"], unique=False)
    op.create_index(op.f("ix_collectionselectiontitle_title"), "collectionselectiontitle", ["title"], unique=False)
    op.create_table(
        "selection",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("modified", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("language", LocaleType(), nullable=True),
        sa.Column("collection_id", sa.UUID(), nullable=True),
        sa.ForeignKeyConstraint(
            ["collection_id"],
            ["collectionselection.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_selection_id"), "selection", ["id"], unique=False)
    op.create_table(
        "selectionterm",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("selection_id", sa.UUID(), nullable=False),
        sa.Column("term", sa.String(), nullable=True),
        sa.Column("language", LocaleType(), nullable=False),
        sa.ForeignKeyConstraint(["selection_id"], ["selection.id"], onupdate="CASCADE", ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_selectionterm_id"), "selectionterm", ["id"], unique=False)
    op.create_index(op.f("ix_selectionterm_term"), "selectionterm", ["term"], unique=False)
    op.create_table(
        "user_selection",
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("selection_id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(
            ["selection_id"],
            ["selection.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("user_id", "selection_id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("user_selection")
    op.drop_index(op.f("ix_selectionterm_term"), table_name="selectionterm")
    op.drop_index(op.f("ix_selectionterm_id"), table_name="selectionterm")
    op.drop_table("selectionterm")
    op.drop_index(op.f("ix_selection_id"), table_name="selection")
    op.drop_table("selection")
    op.drop_index(op.f("ix_collectionselectiontitle_title"), table_name="collectionselectiontitle")
    op.drop_index(op.f("ix_collectionselectiontitle_id"), table_name="collectionselectiontitle")
    op.drop_table("collectionselectiontitle")
    op.drop_index(op.f("ix_collectionselection_name"), table_name="collectionselection")
    op.drop_index(op.f("ix_collectionselection_id"), table_name="collectionselection")
    op.drop_table("collectionselection")
    # ### end Alembic commands ###
