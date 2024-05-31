"""Add token black list model

Revision ID: c11c2aa14b03
Revises: 
Create Date: 2024-05-30 14:40:07.949976

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c11c2aa14b03'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('token_black_list_model', schema=None) as batch_op:
        batch_op.add_column(sa.Column('jti', sa.String(length=200), nullable=False))
        batch_op.add_column(sa.Column('created_on', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('token_black_list_model', schema=None) as batch_op:
        batch_op.drop_column('created_on')
        batch_op.drop_column('jti')

    # ### end Alembic commands ###
