import uuid

from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP

from sqlalchemy import String, Numeric, Integer, Boolean, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from .base import Base
from ..utils.product_domain_validation import ProductDomainValidation

MAX_PRODUCT_NUMBER_LENGTH = 50
MAX_PRODUCT_NAME_LENGTH = 100
MAX_SUPPLIER_NAME_LENGTH = 100
MAX_PRODUCT_DESCRIPTION_LENGTH = 255

class Product(Base):
    __tablename__ = 'tb_products'

    product_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    product_number: Mapped[str] = mapped_column(
        String(MAX_PRODUCT_NUMBER_LENGTH), unique=True, nullable=False
    )

    product_name: Mapped[str] = mapped_column(
        String(MAX_PRODUCT_NAME_LENGTH), nullable=False
    )

    product_price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), nullable=False
    )

    quantity: Mapped[int] = mapped_column(
        Integer, nullable=False
    )

    supplier: Mapped[str] = mapped_column(
        String(MAX_SUPPLIER_NAME_LENGTH), nullable=False
    )

    product_description: Mapped[str | None] = mapped_column(
        String(MAX_PRODUCT_DESCRIPTION_LENGTH), nullable=True
    )

    product_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True
    )

    product_created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )

    product_updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now(), nullable=False
    )

    product_created_by: Mapped[str] = mapped_column(
        String(100), nullable=False
    )

    product_updated_by: Mapped[str] = mapped_column(
        String(100), nullable=False
    )

    @validates('product_number')
    def validate_product_number(self, key: str, value: str) -> str:
        normalized_product_number = ProductDomainValidation.normalize(value)
        upper =  normalized_product_number.upper() if normalized_product_number is not None else None
        return ProductDomainValidation.require_valid_product_number(upper, 'Product Number', MAX_PRODUCT_NUMBER_LENGTH
    )

    @validates('product_name')
    def validate_product_name(self, key: str, value: str) -> str:
        normalized_name = ProductDomainValidation.normalize(value)
        capitalize_case = normalized_name.capitalize() if normalized_name is not None else None
        return ProductDomainValidation.require_non_blank(capitalize_case, 'Product Name', MAX_PRODUCT_NAME_LENGTH
    )

    @validates('product_price')
    def validate_positive_price(self, key: str, value: Decimal | None) -> Decimal:
        normalized_price = None if value is None else value.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        return ProductDomainValidation.require_positive_price(normalized_price, 'Price'
    )

    @validates('quantity')
    def validate_positive_quantity(self, key: str, value: int) -> int:
        return ProductDomainValidation.require_positive_quantity(value, 'Quantity'
    )

    @validates('supplier')
    def validate_supplier(self, key: str, value: str) -> str:
        normalized_supplier = ProductDomainValidation.normalize(value)
        title_case = normalized_supplier.title() if normalized_supplier is not None else None
        return ProductDomainValidation.require_non_blank(title_case, 'Supplier', MAX_SUPPLIER_NAME_LENGTH
    )

    @validates('product_description')
    def validate_description(self, key: str, value: str) -> str | None:
        normalized_description = ProductDomainValidation.normalize(value)
        capitalize_case = normalized_description.capitalize() if normalized_description is not None else None
        return ProductDomainValidation.require_non_blank_if_present(capitalize_case, 'Description', MAX_PRODUCT_DESCRIPTION_LENGTH
    )

    def deactivate(self) -> None:
        self.product_active = False

    def update_fields(self, product_name: str, product_price: Decimal, quantity: int, supplier: str, product_description: str | None) -> None:
        self.product_name = product_name
        self.product_price = product_price
        self.quantity = quantity
        self.supplier = supplier
        self.product_description = product_description

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Product):
            return False
        return self.product_number is not None and self.product_number == other.product_number

    def __hash__(self) -> int:
        return hash(self.product_number)