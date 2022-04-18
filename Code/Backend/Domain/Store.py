from typing import Dict

from Code.Backend.Domain.DiscountPolicy import DiscountPolicy
from Code.Backend.Domain.Permissions import Permissions
from Code.Backend.Domain.Product import Product
from Code.Backend.Domain.StroeInfo import StoreInfo


class Store:
    def __init__(self, founder_id, store_name):
        """
        """
        self.__products: Dict[str, Product] = {}  # {product_id, product object}
        self.__quantities: Dict[str, int] = {}  # {product_id, quantities}
        self.__discount_policy = DiscountPolicy()
        self.__store_info = StoreInfo(founder_id, store_name)
        self.__roles: Dict[str, Permissions] = {founder_id: Permissions(True, None)}  # {user_id, permissions object}

    def get_store_info(self):
        return self.__store_info

    def get_all_products(self) -> list[Product]:
        return list(self.__products.values())

    def get_product(self, product_id, quantity) -> Product:
        """
        returns products if exists and has enough quantity
        else, return None.
        throws ValueError if product does not exists
        """
        if product_id not in self.__products.keys():
            raise ValueError("product does not exist")
        else:
            p_quantity = self.__quantities[product_id]
            if quantity > p_quantity:
                return None
            else:
                return self.__products[product_id]

    def has_access(self, user_id, action):
        return self.__roles[user_id].check_permission(action)

    def update_quantities(self, product_id, quantity):
        self.__quantities[product_id] += quantity

    def add_new_product(self, product_id, quantity):
        self.__products[product_id] = Product(product_id)
        self.__quantities[product_id] = quantity

    def edit_product(self, product_id, name=None, description=None, rating=None):
        product = self.__products[product_id]
        if name is not None:
            product.change_name(name)
        if description is not None:
            product.change_description(description)
        if rating is not None:
            product.change_rating(rating)

    def add_owner(self, user_id: str, new_user_id: str):
        if new_user_id in self.__roles.keys():
            return False
        self.__roles[new_user_id] = Permissions(True, user_id)
        return True

    def add_manager(self, user_id: str, new_manager_id: str):
        if new_manager_id in self.__roles.keys():
            return False
        self.__roles[new_manager_id] = Permissions(False, user_id)
        return True

    def change_permissions(self,user_id,action_number,new_val):
        self.__roles[user_id].set_permission(action_number,new_val)
