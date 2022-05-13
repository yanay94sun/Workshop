from pydantic import BaseModel
from pydantic.class_validators import Optional


class ProductPurchaseRequest(BaseModel):
    product_id: str
    store_id: str
    quantity: int
