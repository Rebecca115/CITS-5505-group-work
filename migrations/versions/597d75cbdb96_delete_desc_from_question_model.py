"""delete desc from question model

Revision ID: 597d75cbdb96
Revises: 335aa3e845a0
Create Date: 2024-05-04 15:34:19.950254

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '597d75cbdb96'
down_revision = '335aa3e845a0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('qa_question', schema=None) as batch_op:
        batch_op.drop_column('desc')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('qa_question', schema=None) as batch_op:
        batch_op.add_column(sa.Column('desc', sa.VARCHAR(length=256), nullable=True))

    # ### end Alembic commands ###
