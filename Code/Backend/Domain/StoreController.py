from Code.Backend.Domain.MemberState import MemberState
from Code.Backend.Domain.Visitor import Visitor
from Code.Backend.Service.Objects.Product_search_filters import Product_search_filters


class StoreController():
    """

    """

    def __init__(self):
        self.stores = {}  # {store id : store object}
        self.inactive_stores = {}  # {store id : store object}

    def get_store_info(self, store_id: str):
        pass

    def search_product(self, by_name=None, by_category=None):  # TODO think about fields
        pass

    def open_store(self, user_id: str, store_name: str):
        pass

    def add_products_to_inventory(self, user_id: str, store_id: str, product_id: str, quantity: int):
        pass

    def remove_products_from_inventory(self, user_id: str, store_id: str, product_id: str, quantity: int):
        pass

    def edit_product_info(self, user_id, store_id, product_id, product_info):
        pass

    def contact_store(self, store_id: str, contact_info):
        pass

    def add_store_owner(self, user_id: str, store_id: str, new_owner_id: str):
        pass

    def remove_store_owner(self, user_id: str, store_id: str, owner_id: str):
        pass

    def add_store_manager(self, user_id: str, store_id: str, new_manager_id: str):
        pass

    def change_manager_permission(self, user_id: str, store_id: str, manager_id: str, new_permission):
        pass

    def remove_store_manager(self, user_id: str, store_id: str, manager_id: str):
        pass

    def close_store(self, user_id: str, store_id: str):
        pass

    def reopen_store(self, user_id: str, store_id: str):
        pass

    def get_store_roles(self, user_id: str, store_id: str):
        pass

    def get_users_messages(self, user_id: str, store_id: str):
        pass

    def reply_users_messages(self, user_id: str, store_id: str, user_contact_info, owner_contact_info):
        pass

    def get_store_purchase_history(self, user_id: str, store_id: str):
        pass

    def get_product(self, product_id, quantity):
        """
        checks if the product is available, and returns its reference.
        returns None if not available
        """
        pass
