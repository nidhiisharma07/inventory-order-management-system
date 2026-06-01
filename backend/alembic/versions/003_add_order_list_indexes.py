"""add indexes for order list search and sort

Revision ID: 003
Revises: 002
Create Date: 2026-06-01

"""
from typing import Sequence, Union

from alembic import op

revision: str = "003"
down_revision: Union[str, None] = "002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_index("ix_orders_created_at", "orders", ["created_at"], unique=False)
    op.create_index("ix_orders_total_amount", "orders", ["total_amount"], unique=False)
    op.create_index("ix_customers_full_name", "customers", ["full_name"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_customers_full_name", table_name="customers")
    op.drop_index("ix_orders_total_amount", table_name="orders")
    op.drop_index("ix_orders_created_at", table_name="orders")
