import uuid

class ProductNumberAlreadyExistsError(Exception):
    def __init__(self, product_number: str) -> None:
        self.product_number = product_number
        super().__init__(f'Product number already exists: {product_number}')

class ProductNotFoundError(Exception):
    def __init__(self, product_id: uuid.UUID) -> None:
        self.product_id = product_id
        super().__init__(f'Product not found with ID: {product_id}')