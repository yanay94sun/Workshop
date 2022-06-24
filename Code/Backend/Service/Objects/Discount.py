from pydantic import BaseModel


class Discount(BaseModel):
    user_id: str
    store_id: str
    discount_price: float
    end_date: str
    product_id: str
    category_name: str
    prodForDiscount: str
    amountForDiscount: int
    min_price_for_discount: int
