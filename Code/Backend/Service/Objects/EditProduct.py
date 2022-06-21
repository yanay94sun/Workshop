from pydantic import BaseModel
from pydantic.class_validators import Optional


class EditProduct(BaseModel):
    id: str
    store_id: str
    product_id: str
    name: Optional[str] = None
    description: Optional[str] = None
    rating: Optional[int] = None
    price: Optional[int] = None
    category: Optional[str] = None


