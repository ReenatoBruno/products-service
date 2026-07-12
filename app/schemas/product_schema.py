from decimal import Decimal

from pydantic import BaseModel, Field, ConfigDict

class ProductRequestDTO(BaseModel):

    product_number: str = Field(max_length=50, pattern=r"^[A-Za-z0-9\-]+$")

    product_name: str = Field(max_length=100)

    product_price: Decimal = Field(ge=Decimal('0.01'), max_digits=12, decimal_places=2)

    quantity: int = Field(ge=0)

    supplier: str = Field(max_length=100)

    product_description: str = Field(max_length=255)