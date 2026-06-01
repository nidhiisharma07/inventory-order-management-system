from collections.abc import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from app.api.deps.auth import get_current_user, require_admin
from app.db.session import get_db
from app.services.auth_service import AuthService
from app.services.customer_service import CustomerService
from app.services.dashboard_service import DashboardService
from app.services.order_service import OrderService
from app.services.product_service import ProductService


def get_auth_service(db: Session = Depends(get_db)) -> Generator[AuthService, None, None]:
    yield AuthService(db)


def get_product_service(db: Session = Depends(get_db)) -> Generator[ProductService, None, None]:
    yield ProductService(db)


def get_customer_service(db: Session = Depends(get_db)) -> Generator[CustomerService, None, None]:
    yield CustomerService(db)


def get_order_service(db: Session = Depends(get_db)) -> Generator[OrderService, None, None]:
    yield OrderService(db)


def get_dashboard_service(db: Session = Depends(get_db)) -> Generator[DashboardService, None, None]:
    yield DashboardService(db)


__all__ = [
    "get_auth_service",
    "get_current_user",
    "get_customer_service",
    "get_dashboard_service",
    "get_order_service",
    "get_product_service",
    "require_admin",
]
