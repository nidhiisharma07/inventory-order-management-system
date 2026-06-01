from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from app.schemas.order import OrderSummaryResponse


class DashboardStatsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    total_orders: int
    total_revenue: Decimal
    recent_orders: list[OrderSummaryResponse]
