from pydantic import BaseModel
from pydantic.class_validators import Optional


class AddNewProduct(BaseModel):
    store_id: str
    product_name: str
    product_description: str
    price: int
    category: str
