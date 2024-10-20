"""kal

Revision ID: 038b4e8b6c24
Revises: 5541875d1ec6
Create Date: 2024-10-16 23:36:43.701648

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '038b4e8b6c24'
down_revision: Union[str, None] = '5541875d1ec6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
