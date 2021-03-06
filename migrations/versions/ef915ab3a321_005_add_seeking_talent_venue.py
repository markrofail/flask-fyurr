"""005 add seeking talent/venue

Revision ID: ef915ab3a321
Revises: 8b495ff9c761
Create Date: 2020-10-10 11:51:18.415776

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "ef915ab3a321"
down_revision = "8b495ff9c761"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("artists", sa.Column("seeking_venue", sa.Boolean(), nullable=False))
    op.add_column(
        "artists", sa.Column("seeking_description", sa.String(), nullable=True)
    )

    op.add_column("venues", sa.Column("seeking_talent", sa.Boolean(), nullable=False))
    op.add_column(
        "venues", sa.Column("seeking_description", sa.String(), nullable=True)
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("venues", "seeking_description")
    op.drop_column("venues", "seeking_talent")

    op.drop_column("artists", "seeking_description")
    op.drop_column("artists", "seeking_venue")
    # ### end Alembic commands ###
