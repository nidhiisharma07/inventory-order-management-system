from decimal import Decimal

from sqlalchemy.orm import Session

from app.core.exceptions import AppError, BusinessRuleError, NotFoundError
from app.models.order import Order, OrderItem, OrderStatus
from app.repositories.customer_repository import CustomerRepository
from app.repositories.order_repository import OrderRepository
from app.repositories.product_repository import ProductRepository
from app.schemas.order import (
    OrderCreate,
    OrderItemResponse,
    OrderListParams,
    OrderResponse,
    OrderSummaryResponse,
    PaginatedOrderListResponse,
)


class OrderService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.order_repository = OrderRepository(db)
        self.product_repository = ProductRepository(db)
        self.customer_repository = CustomerRepository(db)

    def list_orders(self, params: OrderListParams) -> PaginatedOrderListResponse:
        orders, total = self.order_repository.list_paginated(params)
        return PaginatedOrderListResponse(
            total=total,
            page=params.page,
            limit=params.limit,
            data=[self._to_summary(order) for order in orders],
        )

    def get_order(self, order_id: int) -> OrderResponse:
        order = self._get_or_raise(order_id)
        return self._to_response(order)

    def create_order(self, data: OrderCreate) -> OrderResponse:
        """
        Create order inside a single DB transaction.
        Locks product rows, validates stock, deducts inventory, persists order + items.
        Rolls back entirely on any failure.
        """
        customer = self.customer_repository.get_by_id(data.customer_id)
        if customer is None:
            raise NotFoundError(f"Customer with id {data.customer_id} not found")

        product_ids = sorted({item.product_id for item in data.items})
        quantity_by_product = {item.product_id: item.quantity for item in data.items}

        try:
            products = self.product_repository.get_by_ids_for_update(product_ids)
            if len(products) != len(product_ids):
                missing_ids = sorted(set(product_ids) - set(products.keys()))
                raise NotFoundError(f"Product(s) not found: {missing_ids}")

            total_amount = Decimal("0")
            prepared_lines: list[tuple] = []

            for product_id in product_ids:
                quantity = quantity_by_product[product_id]
                product = products[product_id]

                if product.stock_quantity < quantity:
                    raise BusinessRuleError(
                        f"Insufficient stock for '{product.sku}'. "
                        f"Available: {product.stock_quantity}, requested: {quantity}"
                    )

                unit_price = Decimal(str(product.price))
                line_total = unit_price * quantity
                total_amount += line_total
                prepared_lines.append((product, quantity, unit_price, line_total))
                product.stock_quantity -= quantity

            order = Order(
                customer_id=customer.id,
                total_amount=total_amount,
                status=OrderStatus.ACTIVE,
            )
            self.order_repository.create(order)

            for product, quantity, unit_price, line_total in prepared_lines:
                self.db.add(
                    OrderItem(
                        order_id=order.id,
                        product_id=product.id,
                        quantity=quantity,
                        unit_price=unit_price,
                        line_total=line_total,
                    )
                )

            self.db.commit()
            order = self._get_or_raise(order.id)
            return self._to_response(order)
        except AppError:
            self.db.rollback()
            raise
        except Exception:
            self.db.rollback()
            raise

    def cancel_order(self, order_id: int) -> OrderResponse:
        try:
            order = self.order_repository.get_by_id_for_update(order_id)
            if order is None:
                raise NotFoundError(f"Order with id {order_id} not found")

            if order.status == OrderStatus.CANCELLED:
                raise BusinessRuleError("Order is already cancelled")

            product_ids = [item.product_id for item in order.items]
            products = self.product_repository.get_by_ids_for_update(product_ids)

            for item in order.items:
                product = products[item.product_id]
                product.stock_quantity += item.quantity

            order.status = OrderStatus.CANCELLED
            self.db.commit()
            order = self._get_or_raise(order_id)
            return self._to_response(order)
        except AppError:
            self.db.rollback()
            raise
        except Exception:
            self.db.rollback()
            raise

    def get_recent_orders(self, limit: int = 5) -> list[OrderSummaryResponse]:
        orders = self.order_repository.get_recent(limit)
        return [self._to_summary(order) for order in orders]

    def get_order_stats(self) -> tuple[int, Decimal]:
        return self.order_repository.get_aggregate_stats()

    def _get_or_raise(self, order_id: int) -> Order:
        order = self.order_repository.get_by_id(order_id)
        if order is None:
            raise NotFoundError(f"Order with id {order_id} not found")
        return order

    def _to_response(self, order: Order) -> OrderResponse:
        return OrderResponse(
            id=order.id,
            customer_id=order.customer_id,
            customer_name=order.customer.full_name,
            customer_email=order.customer.email,
            status=order.status,
            total_amount=order.total_amount,
            created_at=order.created_at,
            items=[
                OrderItemResponse(
                    id=item.id,
                    product_id=item.product_id,
                    product_name=item.product.name,
                    product_sku=item.product.sku,
                    quantity=item.quantity,
                    unit_price=item.unit_price,
                    line_total=item.line_total,
                )
                for item in order.items
            ],
        )

    def _to_summary(self, order: Order) -> OrderSummaryResponse:
        return OrderSummaryResponse(
            id=order.id,
            customer_id=order.customer_id,
            customer_name=order.customer.full_name,
            status=order.status,
            total_amount=order.total_amount,
            item_count=len(order.items),
            created_at=order.created_at,
        )
