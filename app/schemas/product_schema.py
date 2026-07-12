import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field, ConfigDict

class ProductRequestDTO(BaseModel):

    product_number: str = Field(max_length=50, pattern=r"^[A-Za-z0-9\-]+$")

    product_name: str = Field(max_length=100)

    product_price: Decimal = Field(ge=Decimal('0.01'), max_digits=12, decimal_places=2)

    quantity: int = Field(ge=0)

    supplier: str = Field(max_length=100)

    product_description: str | None = Field(default=None, max_length=255)


class ProductResponseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product_id: uuid.UUID

    product_number: str

    product_name: str

    product_price: Decimal

    quantity: int

    supplier: str

    product_description: str | None

    product_active: bool

    product_created_at: datetime

    product_updated_at: datetime

    product_created_by: str

    product_updated_by: str


class ProductUpdateDTO(BaseModel):

    product_name: str = Field(max_length=100)

    product_price: Decimal = Field(ge=Decimal('0.01'), max_digits=12, decimal_places=2)

    quantity: int = Field(ge=0)

    supplier: str = Field(max_length=100)

    product_description: str | None = Field(default=None, max_length=255)