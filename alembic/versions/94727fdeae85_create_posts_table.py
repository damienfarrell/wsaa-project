"""create posts table

Revision ID: 94727fdeae85
Revises: 
Create Date: 2024-04-13 15:40:50.098851

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '94727fdeae85'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("films", sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
                    sa.Column("title", sa.String(), nullable=False))            
    pass

def downgrade() -> None:
    op.drop_table("films")
    pass
