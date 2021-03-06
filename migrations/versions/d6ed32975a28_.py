"""empty message

Revision ID: d6ed32975a28
Revises: 26dca7f82a8d
Create Date: 2018-06-30 12:27:47.441171

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'd6ed32975a28'
down_revision = '26dca7f82a8d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('article_ibfk_1', 'article', type_='foreignkey')
    op.drop_column('article', 'fav_user_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('article', sa.Column('fav_user_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.create_foreign_key('article_ibfk_1', 'article', 'user', ['fav_user_id'], ['id'])
    # ### end Alembic commands ###
