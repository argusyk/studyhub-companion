"""submissions.is_late

Revision ID: 0004_is_late
Revises: 0003_grades
"""
import sqlalchemy as sa
from alembic import op

revision = "0004_is_late"
down_revision = "0003_grades"
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("submissions") as batch:
        batch.add_column(sa.Column("is_late", sa.Boolean, nullable=False, server_default=sa.false()))


def downgrade() -> None:
    with op.batch_alter_table("submissions") as batch:
        batch.drop_column("is_late")
