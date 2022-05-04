from typing import Dict, List

from Code.Backend.Domain.DiscountPolicy import DiscountPolicy
from Code.Backend.Domain.Permissions import Permissions
from Code.Backend.Domain.Product import Product
from Code.Backend.Domain.Purchase import Purchase
from Code.Backend.Domain.PurchasePolicy import PurchasePolicy
from Code.Backend.Domain.StoreOfficials.StoreFounder import StoreFounder
from Code.Backend.Domain.StoreOfficials.StoreManager import StoreManager
from Code.Backend.Domain.StoreOfficials.StoreOfficial import StoreOfficial
from Code.Backend.Domain.StoreOfficials.StoreOwner import StoreOwner
from Code.Backend.Domain.StroeInfo import StoreInfo


class Store:
    def __init__(self, founder_id, store_name, store_id):
        """
        """
        self.__products: Dict[str, Product] = {}  # {product_id, product object}
        self.__quantities: Dict[str, int] = {}  # {product_id, quantities}
        self.__discount_policy = DiscountPolicy()
        self.__purchase_policy = PurchasePolicy()
        self.__store_info = StoreInfo(founder_id, store_name, store_id)
        self.__officials: Dict[str, StoreOfficial] = {founder_id: StoreFounder(founder_id)}
        # self.__roles: Dict[str, Permissions] = {founder_id: Permissions(True, None)}  # {user_id, permissions object}
        self.__purchase_history: List[Purchase] = []

    def get_store_info(self):
        return self.__store_info

    def get_all_products(self) -> List[Product]:
        if self.__products is not None:
            return list(self.__products.values())
        else:
            return None

    def get_product(self, product_id, quantity) -> Product:
        """
        returns products if exists and has enough quantity
        else, return None.
        throws ValueError if product does not exist
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
        if user_id in self.__officials.keys():
            return self.__officials[user_id].check_permission(action)
        return False

    def update_quantities(self, product_id, quantity):
        self.__quantities[product_id] += quantity

    def add_new_product(self, product_id, quantity):
        self.__products[product_id] = Product(product_id, self.__store_info.ID)
        self.__quantities[product_id] = quantity

    def edit_product(self, product_id, name=None, description=None, rating=None, price=None, category=None):
        product = self.__products[product_id]
        if name is not None:
            product.change_name(name)
        if description is not None:
            product.change_description(description)
        if rating is not None:
            product.change_rating(rating)
        if price is not None:
            product.change_price(price)
        if category is not None:
            product.change_category(category)

    def add_owner(self, user_id: str, new_user_id: str):
        if new_user_id in self.__officials.keys():
            return False
        new_permission = Permissions(self.__officials[user_id])
        self.__officials[new_user_id] = StoreOwner(new_user_id, self.__officials[user_id]
                                                   , new_permission)
        return True

    def add_manager(self, user_id: str, new_manager_id: str):
        if new_manager_id in self.__officials.keys():
            return False
        new_permission = Permissions(self.__officials[user_id])
        self.__officials[new_manager_id] = StoreManager(new_manager_id,
                                                        self.__officials[user_id],
                                                        new_permission)
        return True

    def change_permissions(self, user_id, action_number, new_val):
        self.__officials[user_id].set_permission(action_number, new_val)

    def get_officials(self):
        return self.__officials

    def add_purchase(self, product_name, deal_price, quantity):
        self.__purchase_history.append(Purchase(product_name, deal_price, quantity))

    def get_purchase_history(self):
        return self.__purchase_history

    def get_discount_policy(self):
        return self.__discount_policy
