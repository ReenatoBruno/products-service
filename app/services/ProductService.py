import logging
import uuid

from app.exceptions.ProductException import ProductNumberAlreadyExistsError, ProductNotFoundError
from app.mappers.product_mapper import ProductMapper
from app.models.product import Product
from app.schemas.product_schema import ProductRequestDTO, ProductResponseDTO

from sqlalchemy.exc import IntegrityError

logger = logging.getLogger(__name__)

class ProductService:

    def __init__(self, repository: ProductRepository) -> None:
        self.repository = repository

    def create(self, dto: ProductRequestDTO, created_by: str) -> ProductResponseDTO:

        logger.info('Checking if product number already exists %s', dto.product_number)

        if self.repository.exists_by_product_number(dto.product_number):
            logger.warning(
                'Product number already exists: %s', dto.product_number
            )
            raise ProductNumberAlreadyExistsError(dto.product_number)

        product = ProductMapper.to_entity(dto, created_by)

        try:
            self.repository.save(product)
        except IntegrityError:
            logger.error(
                'Data integrity violation while creating product %s', dto.product_number
            )
            raise ProductNumberAlreadyExistsError(dto.product_number)

        logger.info(
            'Product created successfully with ID: %s and Product number %s', product.product_id, product.product_number
        )
        return ProductMapper.to_response(product)

    def _findy_by_product_id(self, product_id: uuid.UUID) -> Product:

        product = self.repository.find_by_id(product_id)
        if product is None:
            raise ProductNotFoundError(product_id)

        return product