"""grades

Revision ID: 0003_grades
Revises: 0002_submissions
"""
import sqlalchemy as sa
from alembic import op

revision = "0003_grades"
down_revision = "0002_submissions"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "grades",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("submission_id", sa.Integer, sa.ForeignKey("submissions.id"),
                  nullable=False, unique=True),
        sa.Column("raw_score", sa.Float, nullable=False),
        sa.Column("late_days", sa.Integer, nullable=False),
        sa.Column("penalty_percent", sa.Integer, nullable=False),
        sa.Column("penalty", sa.Float, nullable=False),
        sa.Column("final_score", sa.Float, nullable=False),
        sa.Column("status", sa.Enum("draft", "final", name="grade_status"), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("grades")
    sa.Enum(name="grade_status").drop(op.get_bind(), checkfirst=True)
