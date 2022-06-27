from typing import List

from pydantic.main import BaseModel


class ShoppingBasket(BaseModel):
    store_id: str
    product_id: int
    quantity: int

    class Config:
        orm_mode = True


class Notification(BaseModel):
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
    shopping_cart: List[ShoppingBasket] = []
    notifications: List[Notification] = []

    class Config:
        orm_mode = True
