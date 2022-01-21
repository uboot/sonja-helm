"""support missing dependencies

Revision ID: 12c2eb94c088
Revises: 135fda3c3b8e
Create Date: 2022-01-24 09:56:27.952625

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '12c2eb94c088'
down_revision = '135fda3c3b8e'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'missing_recipe',
        sa.Column('build_id', sa.Integer, primary_key=True),
        sa.Column('recipe_id', sa.Integer, primary_key=True)
    )

    op.create_table(
        'missing_package',
        sa.Column('build_id', sa.Integer, primary_key=True),
        sa.Column('package_id', sa.Integer, primary_key=True)
    )


def downgrade():
    op.drop_table('missing_recipe')
    op.drop_table('missing_package')
