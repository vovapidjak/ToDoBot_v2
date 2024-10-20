"""deadline

Revision ID: f65922523634
Revises: 038b4e8b6c24
Create Date: 2024-10-17 00:49:11.824526

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f65922523634'
down_revision: Union[str, None] = '038b4e8b6c24'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
