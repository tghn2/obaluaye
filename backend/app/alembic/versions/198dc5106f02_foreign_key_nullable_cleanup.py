"""Foreign key nullable cleanup

Revision ID: 198dc5106f02
Revises: 3a4500674eef
Create Date: 2023-09-13 13:30:23.062166

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "198dc5106f02"
down_revision = "3a4500674eef"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("node", "theme_id", existing_type=sa.UUID(), nullable=True)
    op.alter_column("resource", "pathway_id", existing_type=sa.UUID(), nullable=True)
    op.alter_column("resource", "theme_id", existing_type=sa.UUID(), nullable=True)
    op.alter_column("resource", "node_id", existing_type=sa.UUID(), nullable=True)
    op.alter_column("response", "group_id", existing_type=sa.UUID(), nullable=True)
    op.alter_column("role", "pathway_id", existing_type=sa.UUID(), nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("role", "pathway_id", existing_type=sa.UUID(), nullable=True)
    op.alter_column("response", "group_id", existing_type=sa.UUID(), nullable=False)
    op.alter_column("resource", "node_id", existing_type=sa.UUID(), nullable=False)
    op.alter_column("resource", "theme_id", existing_type=sa.UUID(), nullable=False)
    op.alter_column("resource", "pathway_id", existing_type=sa.UUID(), nullable=False)
    op.alter_column("node", "theme_id", existing_type=sa.UUID(), nullable=False)
    # ### end Alembic commands ###
