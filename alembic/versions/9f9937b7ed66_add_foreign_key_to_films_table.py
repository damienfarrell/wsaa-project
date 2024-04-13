"""add foreign key to films table

Revision ID: 9f9937b7ed66
Revises: 2902a2290c28
Create Date: 2024-04-13 16:07:36.568571

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9f9937b7ed66'
down_revision: Union[str, None] = '2902a2290c28'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('films', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key('film_users_fk', source_table="films", referent_table="users", local_cols=[
                          'user_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('film_users_fk', table_name="films")
    op.drop_column('films', 'user_id')
    pass
