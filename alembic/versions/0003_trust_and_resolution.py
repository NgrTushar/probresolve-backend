"""Add trust and resolution infrastructure

Revision ID: 0003
Revises: 0002
Create Date: 2026-03-03

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID

revision: str = "0003"
down_revision: Union[str, None] = "0002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # New columns on problems
    op.add_column("problems", sa.Column("is_verified", sa.Boolean(), nullable=False, server_default="false"))
    op.add_column("problems", sa.Column("is_hidden", sa.Boolean(), nullable=False, server_default="false"))
    op.add_column("problems", sa.Column("flags_cleared", sa.Boolean(), nullable=False, server_default="false"))

    # reports table
    op.create_table(
        "reports",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column(
            "problem_id",
            UUID(as_uuid=True),
            sa.ForeignKey("problems.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("fingerprint", sa.String(64), nullable=False),
        sa.Column("reason", sa.String(50), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.UniqueConstraint("problem_id", "fingerprint", name="uq_report_problem_fingerprint"),
    )

    # company_responses table (schema now, feature later)
    op.create_table(
        "company_responses",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column(
            "problem_id",
            UUID(as_uuid=True),
            sa.ForeignKey("problems.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("company_name", sa.String(200), nullable=False),
        sa.Column("responder_email", sa.String(255), nullable=False),
        sa.Column("response_text", sa.Text(), nullable=False),
        sa.Column("is_approved", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )


def downgrade() -> None:
    op.drop_table("company_responses")
    op.drop_table("reports")
    op.drop_column("problems", "flags_cleared")
    op.drop_column("problems", "is_hidden")
    op.drop_column("problems", "is_verified")
