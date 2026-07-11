import uuid

from sqlalchemy import String, Numeric, Integer, Boolean, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from sqlalchemy.testing.schema import Mapped, mapped_column

from .base import Base

class Product(Base):
    __tablename__ = 'tb_products'

    product_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
