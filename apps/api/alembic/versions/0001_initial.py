"""initial: students, labs

Revision ID: 0001_initial
Revises:
"""
import sqlalchemy as sa
from alembic import op

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "students",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("full_name", sa.String(120), nullable=False),
        sa.Column("group_code", sa.String(20), nullable=False),
        sa.Column("email", sa.String(120), nullable=False, unique=True),
    )
    op.create_index("ix_students_group_code", "students", ["group_code"])
    op.create_table(
        "labs",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("number", sa.Integer, nullable=False, unique=True),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("deadline", sa.DateTime(timezone=True), nullable=False),
        sa.Column("max_score", sa.Integer, nullable=False, server_default="100"),
    )


def downgrade() -> None:
    op.drop_table("labs")
    op.drop_index("ix_students_group_code", table_name="students")
    op.drop_table("students")
