from pydantic import BaseModel


class DiscountCompose(BaseModel):
    user_id: str
    store_id: str
    first_discount_id: int
    second_discount_id: int
