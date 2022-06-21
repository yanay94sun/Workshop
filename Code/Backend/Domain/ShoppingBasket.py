from typing import Dict

# from Code.Backend.Domain import Store
from Code.Backend.Domain.MFResponse import Response


class ShoppingBasket:
    def __init__(self, store_ID: str):
        self.__purchase_quantities: Dict[str, int] = {}  # {product_id: quantities}
        self.__store = store_ID

    def add_to_basket(self, product_id: str, quantity: int):
        if product_id in self.__purchase_quantities:
            self.__purchase_quantities[product_id] += quantity
        else:
            self.__purchase_quantities[product_id] = quantity

    def remove_from_basket(self, product_id: str, quantity: int):
        if product_id not in self.__purchase_quantities:
            return Response.from_error("product isn't in the basket")
        if self.__purchase_quantities[product_id] < quantity:
            return Response.from_error("quantity isn't enough for reduction")
        self.__purchase_quantities[product_id] -= quantity
        if self.__purchase_quantities[product_id] == 0:
            self.__purchase_quantities.pop(product_id)
        return Response()

    def get_products_and_quantities(self):
        return self.__purchase_quantities

    def get_store(self):
        return self.__store
