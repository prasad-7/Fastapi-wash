"""add foreign key to bookwashes

Revision ID: 1daa98116849
Revises: 368c85bb795f
Create Date: 2022-11-02 10:29:38.156763

"""
from threading import local
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1daa98116849'
down_revision = '368c85bb795f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_foreign_key('user_wash_fk',source_table='bookwashes',referent_table='users',local_cols=[
                        'user_id'],remote_cols=['id'],ondelete='CASCADE')
    op.create_foreign_key('user_washid_fk', source_table='bookwashes', referent_table='washes', local_cols=[
                          'wash_id'], remote_cols=['id'], ondelete='CASCADE')



def downgrade() -> None:
    op.drop_constraint('user_wash_fk',table_name='bookwashes')
    op.drop_constraint('user_washid_fk', table_name='bookwashes')
