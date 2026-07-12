import uuid

from fastapi import APIRouter, Depends, status, Response, Request
from fastapi_pagination import Page
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, get_current_user
from app.repositories.product_repository import ProductRepository
from app.schemas.product_schema import ProductRequestDTO, ProductResponseDTO, ProductUpdateDTO
from app.services.product_service import ProductService

router = APIRouter(prefix="/products", tags=["Products"])

def get_product_service(db: AsyncSession = Depends(get_db)) -> ProductService:
    repository = ProductRepository(db)
    return ProductService(repository)

@router.post("", response_model=ProductResponseDTO, status_code=status.HTTP_201_CREATED)
async def create_product(
        dto: ProductRequestDTO,
        response: Response,
        request: Request,
        service: ProductService = Depends(get_product_service),
        current_user: str = Depends(get_current_user),
) -> ProductResponseDTO:
    created_product = await service.create(dto, created_by=current_user)
    response.headers["Location"] = f"{request.url}/{created_product.product_id}"
    return created_product

@router.get("/{product_id}", response_model=ProductResponseDTO)
async def get_product(
        product_id: uuid.UUID,
        service: ProductService = Depends(get_product_service),
) -> ProductResponseDTO:
    return await service.get_by_id(product_id)

@router.get("", response_model=Page[ProductResponseDTO])
async def list_products(
        product_name: str | None = None,
        service: ProductService = Depends(get_product_service),
) -> Page[ProductResponseDTO]:
    return await service.get_all(product_name)

@router.put("/{product_id}", response_model=ProductResponseDTO)
async def update_product(
        product_id: uuid.UUID,
        dto: ProductUpdateDTO,
        service: ProductService = Depends(get_product_service),
        current_user: str = Depends(get_current_user),
) -> ProductResponseDTO:
    return await service.update(product_id, dto, updated_by=current_user)

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
        product_id: uuid.UUID,
        service: ProductService = Depends(get_product_service),
) -> None:
    await service.delete(product_id)