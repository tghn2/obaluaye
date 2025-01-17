"""Manual pathway completion

Revision ID: f86cb44cc77e
Revises: 198dc5106f02
Create Date: 2023-10-13 13:20:00.580601

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "f86cb44cc77e"
down_revision = "198dc5106f02"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("group", sa.Column("isComplete", sa.Boolean(), server_default=sa.sql.false(), nullable=False))
    op.add_column("response", sa.Column("validated", sa.Boolean(), server_default=sa.sql.false(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("response", "validated")
    op.drop_column("group", "isComplete")
    # ### end Alembic commands ###
