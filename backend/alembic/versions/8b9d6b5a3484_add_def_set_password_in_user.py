"""add def set_password in User

Revision ID: 8b9d6b5a3484
Revises: 6ae8eb1dc156
Create Date: 2024-07-10 13:31:54.553221

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8b9d6b5a3484'
down_revision: Union[str, None] = '6ae8eb1dc156'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
