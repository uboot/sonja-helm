"""drop revision column

Revision ID: 135fda3c3b8e
Revises: 4cbbca77f13a
Create Date: 2022-01-20 13:55:02.087708

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '135fda3c3b8e'
down_revision = '4cbbca77f13a'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('recipe', 'revision')


def downgrade():
    op.add_column(
        'recipe',
        sa.Column('revision', sa.String(255))
    )
