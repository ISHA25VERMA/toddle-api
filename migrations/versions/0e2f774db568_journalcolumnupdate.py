"""journalColumnUpdate

Revision ID: 0e2f774db568
Revises: f488e33b2f25
Create Date: 2023-06-18 00:46:11.172334

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0e2f774db568'
down_revision = 'f488e33b2f25'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('journals', sa.Column('description', sa.String(length=500), nullable=True))
    op.drop_column('journals', 'decription')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('journals', sa.Column('decription', sa.VARCHAR(length=500), nullable=True))
    op.drop_column('journals', 'description')
    # ### end Alembic commands ###
