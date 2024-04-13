"""add remaining films table columns

Revision ID: 7bc8decc4a83
Revises: 9f9937b7ed66
Create Date: 2024-04-13 16:14:28.895062

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7bc8decc4a83'
down_revision: Union[str, None] = '9f9937b7ed66'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('films', sa.Column(
        'is_watched', sa.Boolean(), nullable=True, server_default='FALSE'),)
    op.add_column('films', sa.Column(
        'rating', sa.Integer(), nullable=True),)
    op.add_column('films', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),)
    pass


def downgrade() -> None:
    op.drop_column('films', 'is_watched')
    op.drop_column('films', 'rating')  
    op.drop_column('films', 'created_at')
    pass
