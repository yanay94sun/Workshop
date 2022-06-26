from datetime import datetime
from typing import List, Dict

from pydantic import BaseModel


class PurchasePolicy(BaseModel):
    pass


class Discount(BaseModel):
    id: int
    discount_on: bool
    end_date: datetime
    type: int
    discount_id: int

    class Config:
        orm_mode = True


class DiscountPolicy(BaseModel):
    store_id: int
    id_counter: int
    discounts: List[Discount]

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
    is_active: bool
    name: str
    founder_username: str
    id_counter: int


class Store(BaseModel):
    store: StoreBase
    purchase_policy: PurchasePolicy
    discount_policy: DiscountPolicy
    products: List[Product] = []
    officials: List[Official]

    class Config:
        orm_mode = True
