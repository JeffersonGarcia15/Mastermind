"""Allowing time_taken to be null in the MatchRecord model

Revision ID: a2cf4fe6791d
Revises: d89d2e5b17d1
Create Date: 2024-12-09 18:40:48.318490

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'a2cf4fe6791d'
down_revision = 'd89d2e5b17d1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('match_records', schema=None) as batch_op:
        batch_op.alter_column('time_taken',
               existing_type=postgresql.INTERVAL(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('match_records', schema=None) as batch_op:
        batch_op.alter_column('time_taken',
               existing_type=postgresql.INTERVAL(),
               nullable=False)

    # ### end Alembic commands ###
