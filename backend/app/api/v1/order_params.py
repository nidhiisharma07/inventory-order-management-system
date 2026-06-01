from typing import Annotated

from fastapi import Query

from app.schemas.order import OrderListParams, OrderSort


def get_order_list_params(
    page: Annotated[int, Query(ge=1, description="Page number (1-based)")] = 1,
    limit: Annotated[int, Query(ge=1, le=100, description="Items per page")] = 10,
    search: Annotated[
        str | None,
        Query(max_length=100, description="Search by customer name, email, or order ID"),
    ] = None,
    sort: Annotated[OrderSort, Query(description="Sort field")] = OrderSort.NEWEST,
) -> OrderListParams:
    return OrderListParams(page=page, limit=limit, search=search, sort=sort)
