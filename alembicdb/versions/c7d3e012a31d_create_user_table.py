"""create user table

Revision ID: c7d3e012a31d
Revises: 
Create Date: 2022-11-01 20:13:47.520059

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c7d3e012a31d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users', sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
                    sa.Column('username', sa.String(),
                              nullable=False, unique=False),
                    sa.Column('email', sa.String(),
                              nullable=False, unique=True),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('otp', sa.Integer(), nullable=True),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              nullable=False, server_default=sa.text('now()')),
                )


def downgrade() -> None:
    op.drop_table('users')