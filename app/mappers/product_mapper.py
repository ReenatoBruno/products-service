from app.models.product import Product
from app.schemas.product_schema import ProductRequestDTO, ProductResponseDTO, ProductUpdateDTO, ProductAdminResponseDTO


class ProductMapper:

    @staticmethod
    def to_entity(dto: ProductRequestDTO, created_by: str) -> Product:
        return Product(
            product_number=dto.product_number,
            product_name=dto.product_name,
            product_price=dto.product_price,
            quantity=dto.quantity,
            supplier=dto.supplier,
            product_description=dto.product_description,
            product_created_by=created_by,
            product_updated_by=created_by,
        )

    @staticmethod
    def to_response(product: Product) -> ProductResponseDTO:
        return ProductResponseDTO(
            product_id=product.product_id,
            product_number=product.product_number,
            product_name=product.product_name,
            product_price=product.product_price,
            quantity=product.quantity,
            supplier=product.supplier,
            product_description=product.product_description,
            product_created_at=product.product_created_at,
            product_updated_at=product.product_updated_at
        )

    @staticmethod
    def to_admin_response(product: Product) -> ProductAdminResponseDTO:
        return ProductAdminResponseDTO(
            product_id=product.product_id,
            product_number=product.product_number,
            product_name=product.product_name,
            product_price=product.product_price,
            quantity=product.quantity,
            supplier=product.supplier,
            product_description=product.product_description,
            product_active=product.product_active,
            product_created_at=product.product_created_at,
            product_updated_at=product.product_updated_at,
            product_created_by=product.product_created_by,
            product_updated_by=product.product_updated_by
        )

    @staticmethod
    def update_entity(product: Product, dto: ProductUpdateDTO, updated_by: str) -> Product:
        product.update_fields(
            product_name=dto.product_name,
            product_price=dto.product_price,
            quantity=dto.quantity,
            supplier=dto.supplier,
            product_description=dto.product_description
        )
        product.product_updated_by=updated_by
        return product
