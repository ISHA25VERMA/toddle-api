"""fileUpload

Revision ID: 8a1c6c0a7cca
Revises: 0e2f774db568
Create Date: 2023-06-18 03:20:46.673827

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8a1c6c0a7cca'
down_revision = '0e2f774db568'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('journals', sa.Column('file_path', sa.String(length=500), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('journals', 'file_path')
    # ### end Alembic commands ###
