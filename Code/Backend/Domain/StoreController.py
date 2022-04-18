from typing import Dict

from Code.Backend.Domain.Actions import Actions
from Code.Backend.Domain.MFResponse import Response
from Code.Backend.Domain.MemberState import MemberState
from Code.Backend.Domain.Product import Product
from Code.Backend.Domain.Store import Store
from Code.Backend.Domain.Visitor import Visitor
from Code.Backend.Service.Objects.Product_search_filters import Product_search_filters


class StoreController:
    """

    """

    def __init__(self):
        self.stores: Dict[str, Store] = {}  # {store id : store object}
        self.inactive_stores: Dict[str, Store] = {}  # {store id : store object}
        self.id_counter = 0

    def get_store_info(self, store_id: str):
        try:
            store = self.__get_store(store_id)
            res = store.get_store_info().__dict__
            products = store.get_all_products()
            res["products"] = list(map(lambda x: x.name, products))
            return Response(value=res)
        except ValueError as e:
            return Response(msg=e.args)

    def get_stores_info(self):
        stores = list(self.stores.values())
        if not stores:
            return Response(msg="No stores in the System")
        res = []
        for store in stores:
            store_info_with_products = store.get_store_info().__dict__
            products = store.get_all_products()
            store_info_with_products["products"] = list(map(lambda x: x.name, products))
            res.append(store_info_with_products)
        return Response(value=res)

    def search_product(self, by_name=None, by_category=None):  # TODO think about fields
        pass

    def open_store(self, user_id: str, store_name: str):
        """
        returns new store's ID
        """
        # check if store's name exists
        for store in self.stores.values():
            if store.get_store_info().store_name == store_name:
                return Response(msg="Store name already exists")
        for store in self.inactive_stores.values():
            if store.get_store_info().store_name == store_name:
                return Response(msg="Store name already exists")
        # create the store
        newStore = Store(user_id, store_name)
        store_id = self.__generate_id()
        self.stores[store_id] = newStore
        return Response(value=store_id)

    def add_products_to_inventory(self, user_id: str, store_id: str, product_id: str, quantity: int):
        # check if number is not negative
        if quantity < 0:
            return Response(msg="Quantity cant be a negative number")

        store = self.__get_store(store_id)

        # check if user has access to this action
        if not store.has_access(user_id, Actions.INVENTORY_ACTION):
            return Response(msg="User does not have access to this action")
        try:
            # check if the product exists. if it is, add new quantity
            product = store.get_product(product_id, 0)
            store.update_quantities(product_id, quantity)
            return Response(value="Added " + str(quantity) + " items of " + product.get_name())

        except ValueError:
            # if product does not exist, create new product
            store.add_new_product(product_id, quantity)
            return Response(value="Added new Product with " + str(quantity) + " items")

    def remove_products_from_inventory(self, user_id: str, store_id: str, product_id: str, quantity: int):
        # check if number is not negative
        if quantity < 0:
            return Response(msg="Quantity cant be a negative number")

        store = self.__get_store(store_id)

        # check if user has access to this action
        if not store.has_access(user_id, Actions.INVENTORY_ACTION):
            return Response(msg="User does not have access to this action")

        # check if product exists
        try:
            product = store.get_product(product_id, quantity)
            # check if there is enough products to remove
            if product is None:
                return Response(msg="Attempt to remove more Items then the existing quantity")
            else:
                store.update_quantities(product_id, -quantity)
                return Response(value="Removed " + str(quantity) + " items of " + product.get_name())

        except ValueError as e:
            return Response(msg=e.args)

    # TODO the real signature should look like this:
    #  def edit_product_info(self, user_id, store_id, name=None, description=None, rating = None ):
    def edit_product_info(self, user_id, store_id, product_id, product_info):
        store = self.__get_store(store_id)

        # check if user has access to this action
        if not store.has_access(user_id, Actions.INVENTORY_ACTION):
            return Response(msg="User does not have access to this action")

        # check if product exists
        try:
            product = store.get_product(product_id, 0)
            if product is None:
                return Response(msg="Product does not exists")
            else:
                store.edit_product(product_id)
                return Response(value="Product was edited")

        except ValueError as e:
            return Response(msg=e.args)

    def add_store_owner(self, user_id: str, store_id: str, new_owner_id: str):
        store = self.__get_store(store_id)

        # check if user has access to this action
        if not store.has_access(user_id, Actions.ADD_STORE_OWNER):
            return Response(msg="User does not have access to this action")

        # check if user is already an owner or store manager
        if not store.add_owner(user_id, new_owner_id):
            return Response(msg="User is already an Owner of this store")
        return Response(value="Made User with id: " + str(user_id) + " an owner")

    def add_store_manager(self, user_id: str, store_id: str, new_manager_id: str):
        store = self.__get_store(store_id)

        # check if user has access to this action
        if not store.has_access(user_id, Actions.ADD_STORE_MANAGER):
            return Response(msg="User does not have access to this action")

        # check if user is already a manager or store owner
        if not store.add_manager(user_id, new_manager_id):
            return Response(msg="User is already an Owner of this store")
        return Response(value="Made User with id: " + str(user_id) + " a manager")

    def change_manager_permission(self, user_id: str, store_id: str, manager_id: str, new_permission):
        store = self.__get_store(store_id)

        # check if user has access to this action
        if not store.has_access(user_id, Actions.ADD_STORE_MANAGER):
            return Response(msg="User does not have access to this action")

        store.change_permissions(manager_id, new_permission, True)  # TODO think about what value is given
        return Response(value="Permissions successfully changed")

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

    def get_product(self, store_id, product_id, quantity):
        """
        checks if the product is available, and returns its reference.
        returns None if not available
        """
        store = self.__get_store(store_id)
        try:
            res = store.get_product(product_id, quantity)
            return res
        except ValueError:  # as e:
            return None  # Response(msg=e.args)

    # ---------------------------------------------------------------------

    def __get_store(self, store_id):
        """
        check if stores exists and return it
        throws ValueError if not exist
        """
        if store_id not in self.stores:
            raise ValueError("Store id does not exist")
        else:
            return self.stores[store_id]

    def __generate_id(self):
        self.id_counter += 1
        return str(self.id_counter)
