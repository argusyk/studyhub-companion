"""submissions

Revision ID: 0002_submissions
Revises: 0001_initial
"""
import sqlalchemy as sa
from alembic import op

revision = "0002_submissions"
down_revision = "0001_initial"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "submissions",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("student_id", sa.Integer, sa.ForeignKey("students.id"), nullable=False),
        sa.Column("lab_id", sa.Integer, sa.ForeignKey("labs.id"), nullable=False),
        sa.Column("submitted_at", sa.DateTime(timezone=True),
                  server_default=sa.func.now(), nullable=False),
        sa.Column("file_url", sa.String(512), nullable=False),
        sa.Column("filename", sa.String(255), nullable=False),
        sa.Column("size_bytes", sa.Integer, nullable=False),
        sa.Column("status", sa.Enum("submitted", "reviewed", "returned",
                                    name="submission_status"), nullable=False),
        sa.Column("score", sa.Integer, nullable=True),
        sa.CheckConstraint("score BETWEEN 0 AND 100", name="ck_submission_score"),
        sa.CheckConstraint("size_bytes > 0", name="ck_submission_size"),
    )
    op.create_index("ix_submissions_student_id", "submissions", ["student_id"])
    op.create_index("ix_submissions_lab_id", "submissions", ["lab_id"])


def downgrade() -> None:
    op.drop_index("ix_submissions_lab_id", table_name="submissions")
    op.drop_index("ix_submissions_student_id", table_name="submissions")
    op.drop_table("submissions")
    sa.Enum(name="submission_status").drop(op.get_bind(), checkfirst=True)
