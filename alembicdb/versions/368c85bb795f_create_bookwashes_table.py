"""create bookwashes table

Revision ID: 368c85bb795f
Revises: 3a0ecbec7c9f
Create Date: 2022-11-01 20:15:14.089827

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '368c85bb795f'
down_revision = '3a0ecbec7c9f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('bookwashes',sa.Column('id', sa.Integer(),primary_key=True,nullable=False),
                    sa.Column('user_id', sa.Integer(),nullable=False),
                    sa.Column('wash_id',sa.Integer(),nullable=False),
                    sa.Column('type',sa.String(),nullable=False),
                    sa.Column('start_time',sa.TIMESTAMP(timezone=False),nullable=False),
                    sa.Column('end_time',sa.TIMESTAMP(timezone=False),nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=False), nullable=False, server_default=sa.text('now()')),
                    sa.Column('completed', sa.Boolean(), server_default='FALSE', nullable=False))



def downgrade() -> None:
    op.drop_table('bookwashes')
