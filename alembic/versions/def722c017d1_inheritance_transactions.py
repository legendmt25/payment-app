"""inheritance transactions

Revision ID: def722c017d1
Revises: 2d5003ec65b6
Create Date: 2022-04-26 12:59:40.798498

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'def722c017d1'
down_revision = '2d5003ec65b6'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "market_transactions", 
        sa.Column("id", sa.Integer, sa.ForeignKey("transactions.id"), primary_key = True),
        sa.Column("shoppingCartId", sa.Integer)
    )
    op.create_table(
        "service_transactions", 
        sa.Column("id", sa.Integer, sa.ForeignKey("transactions.id"), primary_key = True),
        sa.Column("petId", sa.Integer),
    )
    op.create_table(
        "resource_transactions", 
        sa.Column("id", sa.Integer, sa.ForeignKey("transactions.id"), primary_key = True),
        sa.Column("petId", sa.Integer),
    )
    op.create_table(
        "transactions_services_resources",
        sa.Column("id", sa.Integer, sa.ForeignKey("transactions.id"), primary_key = True),
        sa.Column("data_id", sa.Integer, primary_key = True)
    )


def downgrade():
    op.drop_table('market_transactions')
    op.drop_table('service_transactions')
    op.drop_table('resource_transactions')
    op.drop_table('transactions_services_resources')
