from pydantic import BaseModel, validator
from typing import Optional
from enum import Enum

class ProductCategory(Enum):
    FOOD = "food"
    ELECTRONIC = "electonics"
    CLOTHING = "clothing"


class Product(BaseModel):
    id: int
    name: str = "defaultproducts"
    price: float
    tags: list[str] = []
    description: Optional[str] = None
    category: ProductCategory

    @validator("name")
    def name_be_best_titlecase(cls, value):
        if not value:
            raise ValueError("Name ist required")
        if not value[0].isupper():
            raise ValueError("Name muss titlecase sein")
        return value



product = Product(id=1, name="Apfel", price=19.99, category=ProductCategory.FOOD)

product_dict = product.model_dump()

print(product_dict)

product2 = Product(**product_dict)
print(product2)
