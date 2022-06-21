from pydantic import BaseModel


class NewProduct(BaseModel):
    store_id: str
    name: str
    description: str
    price: int
    category: str
    id: str
