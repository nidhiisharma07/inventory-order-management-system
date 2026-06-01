from sqlalchemy.orm import Session

from app.repositories.order_repository import OrderRepository
from app.schemas.dashboard import DashboardStatsResponse
from app.services.order_service import OrderService


class DashboardService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.order_service = OrderService(db)
        self.order_repository = OrderRepository(db)

    def get_stats(self) -> DashboardStatsResponse:
        total_orders, total_revenue = self.order_repository.get_aggregate_stats()
        recent_orders = self.order_service.get_recent_orders(limit=5)

        return DashboardStatsResponse(
            total_orders=total_orders,
            total_revenue=total_revenue,
            recent_orders=recent_orders,
        )
