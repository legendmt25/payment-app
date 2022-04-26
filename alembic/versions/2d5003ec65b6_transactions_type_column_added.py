"""transactions_type_column_added

Revision ID: 2d5003ec65b6
Revises: 0a6829b77976
Create Date: 2022-04-26 12:35:53.705088

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2d5003ec65b6'
down_revision = '0a6829b77976'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'transactions',
        sa.Column('type', sa.String(50))
    )
    pass


def downgrade():
    op.drop_column('transactions', 'type')
