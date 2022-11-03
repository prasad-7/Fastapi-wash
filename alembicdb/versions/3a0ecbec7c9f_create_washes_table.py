"""create washes table

Revision ID: 3a0ecbec7c9f
Revises: 9d7d2bb7aac5
Create Date: 2022-11-01 20:14:56.533956

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3a0ecbec7c9f'
down_revision = '9d7d2bb7aac5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('washes', sa.Column('id',sa.Integer(),primary_key=True,nullable=False),
        sa.Column('type',sa.String(),nullable=False),
        sa.Column('description', sa.String(), nullable=False),
        sa.Column('time_req', sa.Float(), nullable=False),
        sa.Column('price', sa.Float(), nullable=False),
        sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text('now()'))
    )



def downgrade() -> None:
    op.drop_table('washes')
