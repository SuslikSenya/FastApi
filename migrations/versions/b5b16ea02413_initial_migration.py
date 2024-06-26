"""Initial migration

Revision ID: b5b16ea02413
Revises: 
Create Date: 2024-06-16 18:32:48.963115

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b5b16ea02413'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(150), nullable=False),
    sa.Column('permissions', sa.JSON(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(150), nullable=False),
    sa.Column('username', sa.String(150), nullable=False),
    sa.Column('registered_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.Column('hashed_password', sa.String(1024), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('is_superuser', sa.Boolean(), nullable=False),
    sa.Column('is_verified', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('operation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.String(length=100), nullable=True),
    sa.Column('figi', sa.String(length=100), nullable=True),
    sa.Column('instrument_type', sa.String(length=100), nullable=True),
    sa.Column('date', sa.TIMESTAMP(), nullable=True),
    sa.Column('type', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('operation')
    op.drop_table('user')
    op.drop_table('role')
    # ### end Alembic commands ###
