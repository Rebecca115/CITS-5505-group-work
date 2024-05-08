"""add category field

Revision ID: f572485af969
Revises: ae4875e26b0b
Create Date: 2024-05-07 18:30:19.919748

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f572485af969'
down_revision = 'ae4875e26b0b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('qa_task', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date_to_answer', sa.DateTime(), nullable=True))
        batch_op.create_foreign_key("accepted_user_id", 'accounts_user', ['accepted_user_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('qa_task', schema=None) as batch_op:
        batch_op.drop_constraint("accepted_user_id", type_='foreignkey')
        batch_op.drop_column('date_to_answer')

    # ### end Alembic commands ###