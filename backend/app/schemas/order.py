import enum
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models.order import OrderStatus
from app.schemas.pagination import PaginatedResponse, PaginationParams


class OrderSort(str, enum.Enum):
    NEWEST = "newest"
    OLDEST = "oldest"
    HIGHEST_TOTAL = "highest_total"
    LOWEST_TOTAL = "lowest_total"


class OrderListParams(PaginationParams):
    search: str | None = Field(
        default=None,
        max_length=100,
        description="Search by customer name, email, or order ID",
    )
    sort: OrderSort = Field(
        default=OrderSort.NEWEST,
        description="Sort order for results",
    )

    @field_validator("search")
    @classmethod
    def normalize_search(cls, value: str | None) -> str | None:
        if value is None:
            return None
        stripped = value.strip()
        return stripped or None


class OrderItemCreate(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0)


class OrderCreate(BaseModel):
    customer_id: int = Field(..., gt=0)
    items: list[OrderItemCreate] = Field(..., min_length=1)

    @field_validator("items")
    @classmethod
    def validate_items(cls, value: list[OrderItemCreate]) -> list[OrderItemCreate]:
        if not value:
            raise ValueError("Order must contain at least one item")

        product_ids = [item.product_id for item in value]
        if len(product_ids) != len(set(product_ids)):
            raise ValueError("Duplicate products are not allowed in the same order")

        return value


class OrderItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: int
    product_name: str
    product_sku: str
    quantity: int
    unit_price: Decimal
    line_total: Decimal


class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    customer_id: int
    customer_name: str
    customer_email: str
    status: OrderStatus
    total_amount: Decimal
    items: list[OrderItemResponse]
    created_at: datetime


class OrderSummaryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    customer_id: int
    customer_name: str
    status: OrderStatus
    total_amount: Decimal
    item_count: int
    created_at: datetime


class PaginatedOrderListResponse(PaginatedResponse[OrderSummaryResponse]):
    """Paginated list of order summaries."""

    data: list[OrderSummaryResponse]
