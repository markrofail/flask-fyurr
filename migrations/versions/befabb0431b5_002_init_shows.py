"""002 init shows

Revision ID: befabb0431b5
Revises: 3cc1a4da5daf
Create Date: 2020-10-09 19:01:41.507501

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "befabb0431b5"
down_revision = "3cc1a4da5daf"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "shows",
        sa.Column("artist_id", sa.Integer(), nullable=False),
        sa.Column("venue_id", sa.Integer(), nullable=False),
        sa.Column("start_time", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["artist_id"],
            ["artists.id"],
        ),
        sa.ForeignKeyConstraint(
            ["venue_id"],
            ["venues.id"],
        ),
        sa.PrimaryKeyConstraint("artist_id", "venue_id", "start_time"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("shows")
    # ### end Alembic commands ###