"""add order_reports table

Revision ID: d1f5a4d6b2c5
Revises: bd90265be85b
Create Date: 2025-12-09
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "d1f5a4d6b2c5"
down_revision = "bd90265be85b"
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    table_exists = "order_reports" in inspector.get_table_names()

    if not table_exists:
        op.create_table(
            "order_reports",
            sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
            sa.Column("report_at", sa.Date(), nullable=False, index=True),
            sa.Column(
                "order_id", sa.Integer(), sa.ForeignKey("orders.id"), nullable=False
            ),
            sa.Column("count_product", sa.Integer(), nullable=False),
        )

    existing_indexes = {idx["name"] for idx in inspector.get_indexes("order_reports")}

    if "ix_order_reports_report_at" not in existing_indexes:
        op.create_index(
            "ix_order_reports_report_at", "order_reports", ["report_at"], unique=False
        )
    if "ix_order_reports_order_id" not in existing_indexes:
        op.create_index(
            "ix_order_reports_order_id", "order_reports", ["order_id"], unique=False
        )


def downgrade():
    op.drop_index("ix_order_reports_order_id", table_name="order_reports")
    op.drop_index("ix_order_reports_report_at", table_name="order_reports")
    op.drop_table("order_reports")

