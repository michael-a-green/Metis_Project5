"""initial migration

Revision ID: 244569c001f4
Revises: 
Create Date: 2020-12-02 18:34:49.488397

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '244569c001f4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('review_table', 'machine_rating',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    op.alter_column('review_table', 'movie_title',
               existing_type=mysql.VARCHAR(length=500),
               nullable=True)
    op.alter_column('review_table', 'review',
               existing_type=mysql.VARCHAR(length=1000),
               nullable=True)
    op.alter_column('review_table', 'review_title',
               existing_type=mysql.VARCHAR(length=500),
               nullable=True)
    op.alter_column('review_table', 'user_rating',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    op.drop_index('id', table_name='review_table')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('id', 'review_table', ['id'], unique=True)
    op.alter_column('review_table', 'user_rating',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.alter_column('review_table', 'review_title',
               existing_type=mysql.VARCHAR(length=500),
               nullable=False)
    op.alter_column('review_table', 'review',
               existing_type=mysql.VARCHAR(length=1000),
               nullable=False)
    op.alter_column('review_table', 'movie_title',
               existing_type=mysql.VARCHAR(length=500),
               nullable=False)
    op.alter_column('review_table', 'machine_rating',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    # ### end Alembic commands ###
