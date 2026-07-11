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

    product_updated_by = Mapped[str] = mapped_column(
        String(100), nullable=False
    )

    @validates("product_number")
    def validate_product_number(self, key: str, value: str) -> str:
        normalized_product_number = ProductDomainValidation.normalize(value)
        upper =  normalized_product_number.upper() if normalized_product_number is not None else None
        return ProductDomainValidation.require_valid_product_number(upper, "Product Number", MAX_PRODUCT_NUMBER_LENGTH)

    @validates("product_name")
    def validate_product_name(self, key: str, value: str) -> str:
        normalized_name = ProductDomainValidation.normalize(value)
        return ProductDomainValidation.require_non_blank(normalized_name, 'Product Name', MAX_PRODUCT_NAME_LENGTH
    )

