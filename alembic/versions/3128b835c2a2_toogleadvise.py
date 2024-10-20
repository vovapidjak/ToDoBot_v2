"""toogleadvise

Revision ID: 3128b835c2a2
Revises: 3bd6ae3e99eb
Create Date: 2024-10-17 20:22:17.637478

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3128b835c2a2'
down_revision: Union[str, None] = '3bd6ae3e99eb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
