from decimal import Decimal

from sqlalchemy import String, cast, func, or_, select
from sqlalchemy.orm import Session, contains_eager, joinedload

from app.models.customer import Customer
from app.models.order import Order, OrderItem, OrderStatus
from app.repositories.base import BaseRepository
from app.schemas.order import OrderListParams, OrderSort


class OrderRepository(BaseRepository[Order]):
    _SORT_COLUMNS = {
        OrderSort.NEWEST: Order.created_at.desc(),
        OrderSort.OLDEST: Order.created_at.asc(),
        OrderSort.HIGHEST_TOTAL: Order.total_amount.desc(),
        OrderSort.LOWEST_TOTAL: Order.total_amount.asc(),
    }

    def __init__(self, db: Session) -> None:
        super().__init__(db, Order)

    def _detail_options(self):
        return (
            contains_eager(Order.customer),
            joinedload(Order.items).joinedload(OrderItem.product),
        )

    def _list_stmt(self):
        return select(Order).join(Customer).options(*self._detail_options())

    def _apply_search(self, stmt, search: str | None):
        if not search:
            return stmt

        pattern = f"%{search}%"
        conditions = [
            Customer.full_name.ilike(pattern),
            Customer.email.ilike(pattern),
        ]

        if search.isdigit():
            conditions.append(Order.id == int(search))
        else:
            conditions.append(cast(Order.id, String).ilike(pattern))

        return stmt.where(or_(*conditions))

    def _apply_sort(self, stmt, sort: OrderSort):
        order_by = self._SORT_COLUMNS[sort]
        return stmt.order_by(order_by, Order.id.desc())

    def get_by_id(self, order_id: int) -> Order | None:
        stmt = (
            select(Order)
            .where(Order.id == order_id)
            .options(
                joinedload(Order.customer),
                joinedload(Order.items).joinedload(OrderItem.product),
            )
        )
        return self.db.execute(stmt).unique().scalar_one_or_none()

    def get_by_id_for_update(self, order_id: int) -> Order | None:
        stmt = (
            select(Order)
            .where(Order.id == order_id)
            .options(
                joinedload(Order.customer),
                joinedload(Order.items).joinedload(OrderItem.product),
            )
            .with_for_update(of=Order)
        )
        return self.db.execute(stmt).unique().scalar_one_or_none()

    def list_paginated(self, params: OrderListParams) -> tuple[list[Order], int]:
        count_stmt = self._apply_search(
            select(func.count(Order.id)).select_from(Order).join(Customer),
            params.search,
        )
        total = self.db.scalar(count_stmt) or 0

        offset = (params.page - 1) * params.limit
        page_stmt = self._apply_sort(
            self._apply_search(self._list_stmt(), params.search),
            params.sort,
        ).offset(offset).limit(params.limit)

        orders = list(self.db.execute(page_stmt).unique().scalars().all())
        return orders, total

    def create(self, order: Order) -> Order:
        self.db.add(order)
        self.db.flush()
        self.db.refresh(order)
        return order

    def get_recent(self, limit: int = 5) -> list[Order]:
        stmt = (
            self._list_stmt()
            .order_by(Order.created_at.desc(), Order.id.desc())
            .limit(limit)
        )
        return list(self.db.execute(stmt).unique().scalars().all())

    def get_aggregate_stats(self) -> tuple[int, Decimal]:
        total_orders = self.db.scalar(select(func.count(Order.id))) or 0
        total_revenue = self.db.scalar(
            select(func.coalesce(func.sum(Order.total_amount), 0)).where(
                Order.status == OrderStatus.ACTIVE
            )
        )
        return total_orders, Decimal(str(total_revenue or 0))
