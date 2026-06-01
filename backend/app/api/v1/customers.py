from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.api.deps import get_customer_service
from app.api.deps.auth import require_admin
from app.models.user import User
from app.schemas.customer import (
    CustomerCreate,
    CustomerListResponse,
    CustomerResponse,
)
from app.services.customer_service import CustomerService

router = APIRouter(prefix="/customers", tags=["customers"])


@router.get("", response_model=CustomerListResponse)
def list_customers(
    service: CustomerService = Depends(get_customer_service),
) -> CustomerListResponse:
    return service.list_customers()


@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer(
    customer_id: int,
    service: CustomerService = Depends(get_customer_service),
) -> CustomerResponse:
    return service.get_customer(customer_id)


@router.post("", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
def create_customer(
    payload: CustomerCreate,
    service: CustomerService = Depends(get_customer_service),
) -> CustomerResponse:
    return service.create_customer(payload)


@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(
    customer_id: int,
    _admin: Annotated[User, Depends(require_admin)],
    service: CustomerService = Depends(get_customer_service),
) -> None:
    service.delete_customer(customer_id)
