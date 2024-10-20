"""alldelete

Revision ID: 3bd6ae3e99eb
Revises: f65922523634
Create Date: 2024-10-17 01:49:16.024283

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3bd6ae3e99eb'
down_revision: Union[str, None] = 'f65922523634'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
