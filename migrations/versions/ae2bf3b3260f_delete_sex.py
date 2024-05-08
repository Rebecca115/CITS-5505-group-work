"""delete sex

Revision ID: ae2bf3b3260f
Revises: 8400c8201e3e
Create Date: 2024-05-07 19:34:40.498644

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ae2bf3b3260f'
down_revision = '8400c8201e3e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('sex')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('sex', sa.VARCHAR(length=16), nullable=True))

    # ### end Alembic commands ###