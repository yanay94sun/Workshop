from pydantic import BaseModel


class PurchaseRule(BaseModel):
    user_id: str
    store_id: str
    by_category: str
    products_to_have_for_purchase: str
    amount_of_products_to_have: int
    min_price_to_have_for_purchase: int


