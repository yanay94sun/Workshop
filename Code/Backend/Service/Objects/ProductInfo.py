from pydantic import BaseModel
from pydantic.class_validators import Optional


class ProductInfo(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    rating: Optional[int] = None
    price: Optional[int] = None
    category: Optional[str] = None
