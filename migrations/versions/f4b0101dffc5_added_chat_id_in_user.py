"""Added chat_id in User

Revision ID: f4b0101dffc5
Revises: 439af53e794d
Create Date: 2024-11-29 13:05:44.546096

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f4b0101dffc5'
down_revision: Union[str, None] = '439af53e794d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Users', sa.Column('chat_id', sa.BigInteger(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Users', 'chat_id')
    # ### end Alembic commands ###