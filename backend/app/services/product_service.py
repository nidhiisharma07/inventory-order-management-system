from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.models.product import Product
from app.repositories.product_repository import ProductRepository
from app.schemas.product import ProductCreate, ProductListResponse, ProductResponse, ProductUpdate


class ProductService:
    def __init__(self, db: Session) -> None:
        self.repository = ProductRepository(db)
        self.db = db

    def list_products(self) -> ProductListResponse:
        products = self.repository.get_all()
        return ProductListResponse(
            items=[ProductResponse.model_validate(p) for p in products],
            total=len(products),
        )

    def get_product(self, product_id: int) -> ProductResponse:
        product = self._get_or_raise(product_id)
        return ProductResponse.model_validate(product)

    def create_product(self, data: ProductCreate) -> ProductResponse:
        product = self.repository.create(data)
        self.db.commit()
        return ProductResponse.model_validate(product)

    def update_product(self, product_id: int, data: ProductUpdate) -> ProductResponse:
        product = self._get_or_raise(product_id)
        if not data.model_dump(exclude_unset=True):
            return ProductResponse.model_validate(product)
        product = self.repository.update(product, data)
        self.db.commit()
        return ProductResponse.model_validate(product)

    def delete_product(self, product_id: int) -> None:
        product = self._get_or_raise(product_id)
        self.repository.delete(product)
        self.db.commit()

    def _get_or_raise(self, product_id: int) -> Product:
        product = self.repository.get_by_id(product_id)
        if product is None:
            raise NotFoundError(f"Product with id {product_id} not found")
        return product
