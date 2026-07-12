import logging
import uuid

from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select

from app.exceptions.product_exception import ProductNumberAlreadyExistsError, ProductNotFoundError
from app.mappers.product_mapper import ProductMapper
from app.models.product import Product
from app.repositories.ProductRepository import ProductRepository
from app.schemas.product_schema import ProductRequestDTO, ProductResponseDTO, ProductUpdateDTO

from sqlalchemy.exc import IntegrityError

logger = logging.getLogger(__name__)

class ProductService:

    def __init__(self, repository: ProductRepository) -> None:
        self.repository = repository

    async def create(self, dto: ProductRequestDTO, created_by: str) -> ProductResponseDTO:

        logger.info('Checking if product number already exists %s', dto.product_number)

        await self._ensure_product_number_available(dto.product_number)

        product = ProductMapper.to_entity(dto, created_by)

        await self._save_created_product(product)

        return ProductMapper.to_response(product)

    async def get_by_id(self, product_id: uuid.UUID) -> ProductResponseDTO:

        logger.info('Fetching products with ID: %s', product_id)

        product = await self._find_by_product_id(product_id)

        return ProductMapper.to_response(product)

    async def get_all(self, product_name: str | None) -> Page[ProductResponseDTO]:

        logger.debug("Fetching all products with filter product name %s", product_name)

        query = select(Product)
        normalized_product_name = product_name.strip() if product_name else None

        if normalized_product_name:
            query = query.where(Product.product_name.ilike(f"%{normalized_product_name}%"))

        return await paginate(
            self.repository.session,
            query,
            transformer=lambda items: [ProductMapper.to_response(p) for p in items],
        )

    async def update(self, product_id: uuid.UUID, dto: ProductUpdateDTO, updated_by: str) -> ProductResponseDTO:

        logger.info("Updating product with ID: %s", product_id)

        product = await self._find_by_product_id(product_id)

        ProductMapper.update_entity(product, dto, updated_by)

        await self.repository.save(product)

        logger.info("Product updated successfully with ID: %s", product_id)

        return ProductMapper.to_response(product)

    async def delete(self, product_id: uuid.UUID) -> None:

        logger.info("Deleting product with ID: %s", product_id)

        product = await self._find_by_product_id(product_id)

        product.deactivate()

        await self.repository.save(product)

        logger.info("Product deleted successfully with ID: %s", product_id)

    async def _ensure_product_number_available(self, product_number: str) -> None:
        if await self.repository.exists_by_product_number(product_number):
            logger.warning("Product number already exists: %s", product_number)
            raise ProductNumberAlreadyExistsError(product_number)

    async def _save_created_product(self, product: Product) -> None:
        try:
            await self.repository.save(product)
        except IntegrityError as error:
            logger.error(
                "Data integrity violation while creating product %s",
                product.product_number,
            )
            raise ProductNumberAlreadyExistsError(product.product_number) from error

    async def _find_by_product_id(self, product_id: uuid.UUID) -> Product:
        product = await self.repository.find_by_id(product_id)

        if product is None:
            raise ProductNotFoundError(product_id)

        return product