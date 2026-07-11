import re

class ProductDomainValidation:

    @staticmethod
    def normalize(value: str | None) -> str | None:
        if value is None:
            return None
        return value.strip()

    @staticmethod
    def require_valid_product_number(value: str | None,
                                     field: str,
                                     max_length: int) -> str:

        cleaned = ProductDomainValidation.require_non_blank(value, field, max_length)

        if not re.match(r"^[A-Za-z0-9\-]+$", cleaned):
            raise ValueError(f'{field} must contain only letters, numbers and hyphens')

        return cleaned

    @staticmethod
    def require_non_blank(value: str | None,
                          field: str,
                          max_length: int) -> str:

        if value is None:
            raise ValueError(f'{field} is required')

        if not value.strip():
            raise ValueError(f'{field} must not be blank')

        if len(value) > max_length:
            raise ValueError(f'{field} must not exceed {max_length} characters')

        return value