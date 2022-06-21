from pydantic import BaseModel


class ProductPurchaseRequest(BaseModel):
    store_id: str
    product_id: str
    quantity: int
