from pydantic import BaseModel


class AddProduct(BaseModel):
    store_id: str
    product_id: str
    quantity: int
    id: str
