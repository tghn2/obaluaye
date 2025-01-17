"""Deeper authentication

Revision ID: 8188d671489a
Revises: c4f38069dc24
Create Date: 2023-01-01 15:31:40.986707

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "8188d671489a"
down_revision = "c4f38069dc24"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("user", sa.Column("created", sa.DateTime(), server_default=sa.text("now()"), nullable=False))
    op.add_column("user", sa.Column("modified", sa.DateTime(), server_default=sa.text("now()"), nullable=False))
    op.add_column("user", sa.Column("totp_secret", sa.String(), nullable=True))
    op.add_column("user", sa.Column("totp_counter", sa.Integer(), nullable=True))
    op.alter_column("user", "hashed_password", existing_type=sa.VARCHAR(), nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("user", "hashed_password", existing_type=sa.VARCHAR(), nullable=False)
    op.drop_column("user", "totp_counter")
    op.drop_column("user", "totp_secret")
    op.drop_column("user", "modified")
    op.drop_column("user", "created")
    # ### end Alembic commands ###
