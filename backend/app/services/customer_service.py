from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.models.customer import Customer
from app.repositories.customer_repository import CustomerRepository
from app.schemas.customer import (
    CustomerCreate,
    CustomerListResponse,
    CustomerResponse,
)


class CustomerService:
    def __init__(self, db: Session) -> None:
        self.repository = CustomerRepository(db)
        self.db = db

    def list_customers(self) -> CustomerListResponse:
        customers = self.repository.get_all()
        return CustomerListResponse(
            items=[CustomerResponse.model_validate(c) for c in customers],
            total=len(customers),
        )

    def get_customer(self, customer_id: int) -> CustomerResponse:
        customer = self._get_or_raise(customer_id)
        return CustomerResponse.model_validate(customer)

    def create_customer(self, data: CustomerCreate) -> CustomerResponse:
        customer = self.repository.create(data)
        self.db.commit()
        return CustomerResponse.model_validate(customer)

    def delete_customer(self, customer_id: int) -> None:
        customer = self._get_or_raise(customer_id)
        self.repository.delete(customer)
        self.db.commit()

    def _get_or_raise(self, customer_id: int) -> Customer:
        customer = self.repository.get_by_id(customer_id)
        if customer is None:
            raise NotFoundError(f"Customer with id {customer_id} not found")
        return customer
