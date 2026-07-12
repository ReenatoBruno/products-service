import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.product import Product


class ProductRepository:

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def find_by_id(self, product_id: uuid.UUID) -> Product | None:

        result = await self.session.execute(
            select(Product).where(
                Product.product_id == product_id,
                Product.product_active.is_(True),
            )
        )
        return result.scalar_one_or_none()

    async def exists_by_product_number(self, product_number: str) -> bool:

        result = await self.session.execute(
            select(Product.product_id).where(
                Product.product_number == product_number,
                Product.product_active.is_(True),
            )
        )
        return result.scalar_one_or_none() is not None

    async def save(self, product: Product) -> Product:

        self.session.add(product)
        await self.session.flush()
        await self.session.refresh(product)
        return product