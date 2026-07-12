from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi_pagination import add_pagination

from app.exceptions.product_exception import (ProductNotFoundError,ProductNumberAlreadyExistsError,)
from app.routers.product_router import router as product_router

app = FastAPI(title="Products Service", version="0.1.0")

app.include_router(product_router)

add_pagination(app)

@app.exception_handler(ProductNotFoundError)
async def product_not_found_handler(request: Request, exc: ProductNotFoundError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc)},
    )

@app.exception_handler(ProductNumberAlreadyExistsError)
async def product_number_already_exists_handler(request: Request, exc: ProductNumberAlreadyExistsError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": str(exc)},
    )