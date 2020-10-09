"""001 init db

Revision ID: 3cc1a4da5daf
Revises:
Create Date: 2020-10-09 18:09:49.014493

"""
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = "3cc1a4da5daf"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "artists",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("city", sa.String(length=120), nullable=True),
        sa.Column("state", sa.String(length=120), nullable=True),
        sa.Column("phone", sa.String(length=120), nullable=True),
        sa.Column("genres", sa.String(length=120), nullable=True),
        sa.Column("image_link", sa.String(length=500), nullable=True),
        sa.Column("facebook_link", sa.String(length=120), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "venues",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("city", sa.String(length=120), nullable=True),
        sa.Column("state", sa.String(length=120), nullable=True),
        sa.Column("address", sa.String(length=120), nullable=True),
        sa.Column("phone", sa.String(length=120), nullable=True),
        sa.Column("image_link", sa.String(length=500), nullable=True),
        sa.Column("facebook_link", sa.String(length=120), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("venues")
    op.drop_table("artists")
    # ### end Alembic commands ###