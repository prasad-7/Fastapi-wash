"""create admin table

Revision ID: 9d7d2bb7aac5
Revises: c7d3e012a31d
Create Date: 2022-11-01 20:14:24.070131

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9d7d2bb7aac5'
down_revision = 'c7d3e012a31d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('admin', sa.Column('id', sa.Integer(),
                             primary_key=True, nullable=False),
                        sa.Column('email', sa.String(),
                              nullable=False, unique=True),
                        sa.Column('password', sa.String(), nullable=False),
                        sa.Column('otp', sa.Integer(), nullable=True),
                        sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              nullable=False, server_default=sa.text('now()'))
                    )


def downgrade() -> None:
    op.drop_table('admin')
