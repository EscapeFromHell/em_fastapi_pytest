"""init_migration

Revision ID: bb6a7598b44a
Revises: 
Create Date: 2024-04-11 12:26:38.212020

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bb6a7598b44a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('spimex_trading_results',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('exchange_product_id', sa.String(), nullable=False),
    sa.Column('exchange_product_name', sa.String(), nullable=False),
    sa.Column('oil_id', sa.String(), nullable=False),
    sa.Column('delivery_basis_id', sa.String(), nullable=False),
    sa.Column('delivery_basis_name', sa.String(), nullable=False),
    sa.Column('delivery_type_id', sa.String(), nullable=False),
    sa.Column('volume', sa.String(), nullable=False),
    sa.Column('total', sa.String(), nullable=False),
    sa.Column('count', sa.String(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('created_on', sa.DateTime(), nullable=False),
    sa.Column('updated_on', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('spimex_trading_results')
    # ### end Alembic commands ###