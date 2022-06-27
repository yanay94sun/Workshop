from datetime import datetime
from typing import List, Dict

from pydantic import BaseModel


class PurchaseRule(BaseModel):
    id: int
    store_id: int
    product_id: int
    quantity: int
    min_price_to_have: int
    category: str
    purchase_policy_id: int

    class Config:
        orm_mode = True


class ComplexPurchaseRule(BaseModel):
    id: int
    first_rule_id: int
    second_rule_id: int
    type_: int  # or/and...
    purchase_policy_id: int

    class Config:
        orm_mode = True


class PurchasePolicy(BaseModel):
    policy_id: int
    store_id: int
    id_counter: int
    purchase_rules: List[PurchaseRule] = []
    complex_purchase_rules: List[ComplexPurchaseRule] = []

    class Config:
        orm_mode = True


class Discount(BaseModel):
    id: int
    store_id: int
    discount_on: bool
    end_date: datetime
    type: int
    discount_policy_id: int
    product_id: int
    min_count_of_product: int
    min_price_of_product: int
    is_visible: bool
    discount_value: float

    class Config:
        orm_mode = True


class ComplexDiscount(BaseModel):
    id: int
    first_discount: int
    second_discount: int
    type_: int  # or/and/cond...
    discount_policy_id: int

    class Config:
        orm_mode = True


class DiscountPolicy(BaseModel):
    policy_id: int
    store_id: int
    id_counter: int
    discounts: List[Discount] = []
    complex_discounts: List[ComplexDiscount] = []

    class Config:
        orm_mode = True


class Product(BaseModel):
    product_id: int
    name: str
    description: str
    rating: int
    price: int
    category: str
    quantity: int
    store_id: int

    class Config:
        orm_mode = True


class Official(BaseModel):
    username: str
    appointee: str
    INVENTORY_ACTION: bool
    CHANGE_MANAGER_PERMISSION: bool
    ADD_STORE_MANAGER: bool
    ADD_STORE_OWNER: bool
    GET_STORE_PURCHASE_HISTORY: bool
    CLOSE_STORE: bool
    GET_STORE_ROLES: bool
    PURCHASE_MANAGEMENT: bool
    DISCOUNT_MANAGEMENT: bool
    is_owner: bool

    class Config:
        orm_mode = True


class StoreBase(BaseModel):
    store_id: str
    name: str
    is_active: bool
    founder_username: str
    id_counter: int

    class Config:
        orm_mode = True


class Store(BaseModel):
    store: StoreBase
    purchase_policy: PurchasePolicy
    discount_policy: DiscountPolicy
    products: List[Product] = []
    officials: List[Official]

    class Config:
        orm_mode = True
