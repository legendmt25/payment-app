"""empty message

Revision ID: 0a6829b77976
Revises: 
Create Date: 2022-04-26 12:30:55.742496

"""
from enum import Enum
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0a6829b77976'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "transactions",
        sa.Column("id", sa.Integer, primary_key = True, index = True),
        sa.Column("userId", sa.Integer),
        sa.Column("createdAt", sa.Date),
        sa.Column("price", sa.Numeric),
        sa.Column("status", sa.Enum(Enum)),
    )


def downgrade():
    op.drop_table("transactions")
