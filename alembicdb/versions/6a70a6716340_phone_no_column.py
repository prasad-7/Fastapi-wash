"""phone_no column

Revision ID: 6a70a6716340
Revises: 1daa98116849
Create Date: 2022-11-08 00:31:48.627396

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6a70a6716340'
down_revision = '1daa98116849'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column('phone_number',sa.String(),nullable=False))
    pass

def downgrade() -> None:
    op.drop_column('users','phone_number')
    pass