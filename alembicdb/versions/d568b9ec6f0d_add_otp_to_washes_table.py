"""add_otp to washes table

Revision ID: d568b9ec6f0d
Revises: 
Create Date: 2022-10-28 19:19:14.569881

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd568b9ec6f0d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('washes', sa.Column('otp', sa.Integer(), nullable=True))


def downgrade() -> None:
    op.drop_column('washes','otp')
