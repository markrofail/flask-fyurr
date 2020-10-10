"""004 3NF split contact info

Revision ID: 8b495ff9c761
Revises: 03dd58441e73
Create Date: 2020-10-09 22:21:13.791376

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "8b495ff9c761"
down_revision = "03dd58441e73"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    # create table ContactInfo
    op.create_table(
        "contact_info",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("phone", sa.String(), nullable=False),
        sa.Column("image_link", sa.String(), nullable=False),
        sa.Column("website", sa.String(), nullable=True),
        sa.Column("facebook_link", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )

    # add link to artists
    op.add_column("artists", sa.Column("contact_info_id", sa.Integer(), nullable=False))
    op.create_unique_constraint(None, "artists", ["contact_info_id"])
    op.create_foreign_key(None, "artists", "contact_info", ["contact_info_id"], ["id"])

    # add link to venues
    op.add_column("venues", sa.Column("contact_info_id", sa.Integer(), nullable=False))
    op.create_unique_constraint(None, "venues", ["contact_info_id"])
    op.create_foreign_key(None, "venues", "contact_info", ["contact_info_id"], ["id"])

    # remove redundant columns from artist
    op.drop_column("artists", "image_link")
    op.drop_column("artists", "facebook_link")
    op.drop_column("artists", "phone")

    # remove redundant columns from venues
    op.drop_column("venues", "image_link")
    op.drop_column("venues", "facebook_link")
    op.drop_column("venues", "phone")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    # add old columns to venues
    op.add_column(
        "venues",
        sa.Column("phone", sa.VARCHAR(length=120), autoincrement=False, nullable=True),
    )
    op.add_column(
        "venues",
        sa.Column(
            "facebook_link", sa.VARCHAR(length=120), autoincrement=False, nullable=True
        ),
    )
    op.add_column(
        "venues",
        sa.Column(
            "image_link", sa.VARCHAR(length=500), autoincrement=False, nullable=True
        ),
    )

    # add old columns to artist
    op.add_column(
        "artists",
        sa.Column("phone", sa.VARCHAR(length=120), autoincrement=False, nullable=True),
    )
    op.add_column(
        "artists",
        sa.Column(
            "facebook_link", sa.VARCHAR(length=120), autoincrement=False, nullable=True
        ),
    )
    op.add_column(
        "artists",
        sa.Column(
            "image_link", sa.VARCHAR(length=500), autoincrement=False, nullable=True
        ),
    )

    # remove link venues to contact info
    op.drop_constraint(None, "venues", type_="foreignkey")
    op.drop_constraint(None, "venues", type_="unique")
    op.drop_column("venues", "contact_info_id")

    # remove link artist to contact info
    op.drop_constraint(None, "artists", type_="foreignkey")
    op.drop_constraint(None, "artists", type_="unique")
    op.drop_column("artists", "contact_info_id")

    # drop contact info
    op.drop_table("contact_info")
    # ### end Alembic commands ###