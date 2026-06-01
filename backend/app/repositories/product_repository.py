from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.exceptions import ConflictError
from app.models.product import Product
from app.repositories.base import BaseRepository
from app.schemas.product import ProductCreate, ProductUpdate


class ProductRepository(BaseRepository[Product]):
    def __init__(self, db: Session) -> None:
        super().__init__(db, Product)

    def get_by_id(self, product_id: int) -> Product | None:
        return self.db.get(Product, product_id)

    def get_by_sku(self, sku: str) -> Product | None:
        stmt = select(Product).where(Product.sku == sku)
        return self.db.execute(stmt).scalar_one_or_none()

    def get_all(self) -> list[Product]:
        stmt = select(Product).order_by(Product.created_at.desc())
        return list(self.db.execute(stmt).scalars().all())

    def get_by_ids_for_update(self, product_ids: list[int]) -> dict[int, Product]:
        if not product_ids:
            return {}
        stmt = (
            select(Product)
            .where(Product.id.in_(product_ids))
            .with_for_update()
        )
        products = self.db.execute(stmt).scalars().all()
        return {product.id: product for product in products}

    def create(self, data: ProductCreate) -> Product:
        product = Product(
            name=data.name,
            sku=data.sku,
            price=data.price,
            stock_quantity=data.stock_quantity,
        )
        self.db.add(product)
        try:
            self.db.flush()
            self.db.refresh(product)
        except IntegrityError as exc:
            self.db.rollback()
            raise ConflictError(f"Product with SKU '{data.sku}' already exists") from exc
        return product

    def update(self, product: Product, data: ProductUpdate) -> Product:
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(product, field, value)
        try:
            self.db.flush()
            self.db.refresh(product)
        except IntegrityError as exc:
            self.db.rollback()
            sku = update_data.get("sku", product.sku)
            raise ConflictError(f"Product with SKU '{sku}' already exists") from exc
        return product

    def delete(self, product: Product) -> None:
        self.db.delete(product)
        self.db.flush()
