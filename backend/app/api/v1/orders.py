from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.api.deps import get_order_service
from app.api.deps.auth import require_admin
from app.models.user import User
from app.api.v1.order_params import get_order_list_params
from app.schemas.order import (
    OrderCreate,
    OrderListParams,
    OrderResponse,
    PaginatedOrderListResponse,
)
from app.services.order_service import OrderService

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("", response_model=PaginatedOrderListResponse)
def list_orders(
    params: Annotated[OrderListParams, Depends(get_order_list_params)],
    service: OrderService = Depends(get_order_service),
) -> PaginatedOrderListResponse:
    return service.list_orders(params)


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    service: OrderService = Depends(get_order_service),
) -> OrderResponse:
    return service.get_order(order_id)


@router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
    payload: OrderCreate,
    service: OrderService = Depends(get_order_service),
) -> OrderResponse:
    return service.create_order(payload)


@router.delete("/{order_id}", response_model=OrderResponse)
def cancel_order(
    order_id: int,
    _admin: Annotated[User, Depends(require_admin)],
    service: OrderService = Depends(get_order_service),
) -> OrderResponse:
    """Cancel order and restore inventory."""
    return service.cancel_order(order_id)
