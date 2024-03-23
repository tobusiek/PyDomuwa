"""init tables

Revision ID: bb2697c66922
Revises: b8835f791ee2
Create Date: 2023-10-06 20:10:09.624948

"""

from typing import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = "bb2697c66922"
down_revision: Union[str, None] = "b8835f791ee2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
