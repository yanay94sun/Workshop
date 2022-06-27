from typing import List

from pydantic.main import BaseModel


class ShoppingBasketItem(BaseModel):
    """
    represent a single item in a shopping basket
    """
    store_id: str
    product_id: int
    quantity: int

    class Config:
        orm_mode = True


class Notification(BaseModel):
    id: int
    message: str

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True


class User(BaseModel):
    user: UserBase
    shopping_cart: List[ShoppingBasketItem] = []
    notifications: List[Notification] = []

    class Config:
        orm_mode = True
