"""Upgrading db to have the new changes

Revision ID: f2c5484e37ac
Revises: de093b6f0075
Create Date: 2024-12-10 18:59:53.061211

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f2c5484e37ac'
down_revision = 'de093b6f0075'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('games',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('difficulty', sa.Enum('easy', 'medium', 'hard', name='difficulty'), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('solution', sa.String(length=10), nullable=False),
    sa.Column('fallback_used', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('games', schema=None) as batch_op:
        batch_op.create_index('game_user_id_index', ['user_id'], unique=False)

    op.create_table('attempts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('game_id', sa.UUID(), nullable=True),
    sa.Column('guess', sa.String(length=10), nullable=False),
    sa.Column('hints', sa.String(length=255), nullable=False),
    sa.Column('time', sa.TIMESTAMP(), nullable=True),
    sa.ForeignKeyConstraint(['game_id'], ['games.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('attempts', schema=None) as batch_op:
        batch_op.create_index('attempt_game_id_index', ['game_id'], unique=False)

    op.create_table('match_records',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('game_id', sa.UUID(), nullable=True),
    sa.Column('result', sa.Enum('win', 'lose', name='result'), nullable=False),
    sa.Column('score', sa.Integer(), nullable=False),
    sa.Column('time_taken', sa.Interval(), nullable=True),
    sa.ForeignKeyConstraint(['game_id'], ['games.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('match_records', schema=None) as batch_op:
        batch_op.create_index('match_record_score_index', ['score'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('match_records', schema=None) as batch_op:
        batch_op.drop_index('match_record_score_index')

    op.drop_table('match_records')
    with op.batch_alter_table('attempts', schema=None) as batch_op:
        batch_op.drop_index('attempt_game_id_index')

    op.drop_table('attempts')
    with op.batch_alter_table('games', schema=None) as batch_op:
        batch_op.drop_index('game_user_id_index')

    op.drop_table('games')
    op.drop_table('users')
    # ### end Alembic commands ###
