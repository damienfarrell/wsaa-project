"""add comment column to films table

Revision ID: b9e3ca9e3ee0
Revises: 94727fdeae85
Create Date: 2024-04-13 15:53:58.857809

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b9e3ca9e3ee0'
down_revision: Union[str, None] = '94727fdeae85'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("films", sa.Column("comment", sa.String(), nullable=True))
    
    pass


def downgrade() -> None:
    op.drop_column("films", "comment")
    pass
