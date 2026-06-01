from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.exceptions import ConflictError
from app.models.customer import Customer
from app.repositories.base import BaseRepository
from app.schemas.customer import CustomerCreate


class CustomerRepository(BaseRepository[Customer]):
    def __init__(self, db: Session) -> None:
        super().__init__(db, Customer)

    def get_by_id(self, customer_id: int) -> Customer | None:
        return self.db.get(Customer, customer_id)

    def get_all(self) -> list[Customer]:
        stmt = select(Customer).order_by(Customer.created_at.desc())
        return list(self.db.execute(stmt).scalars().all())

    def create(self, data: CustomerCreate) -> Customer:
        customer = Customer(
            full_name=data.full_name,
            email=data.email,
            phone=data.phone,
        )
        self.db.add(customer)
        try:
            self.db.flush()
            self.db.refresh(customer)
        except IntegrityError as exc:
            self.db.rollback()
            raise ConflictError(f"Customer with email '{data.email}' already exists") from exc
        return customer

    def delete(self, customer: Customer) -> None:
        self.db.delete(customer)
        try:
            self.db.flush()
        except IntegrityError as exc:
            self.db.rollback()
            raise ConflictError(
                "Cannot delete customer with existing orders"
            ) from exc
