from pydantic import BaseModel
from pydantic.class_validators import Optional


class ProductSearchFilters(BaseModel):
    text: str
    by_name: bool = True
    by_category: Optional[bool] = None
    filter_type: Optional[bool] = None
    filter_value: Optional[bool] = None
