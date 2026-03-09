"""add poster_name, location_state, date_of_incident to problems

Revision ID: 0002
Revises: 0001
Create Date: 2026-03-02

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0002"
down_revision: Union[str, None] = "0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("problems", sa.Column("poster_name", sa.Text(), nullable=True))
    op.add_column("problems", sa.Column("location_state", sa.Text(), nullable=True))
    op.add_column("problems", sa.Column("date_of_incident", sa.Date(), nullable=True))


def downgrade() -> None:
    op.drop_column("problems", "date_of_incident")
    op.drop_column("problems", "location_state")
    op.drop_column("problems", "poster_name")
