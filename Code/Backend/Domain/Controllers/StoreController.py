from typing import Dict

from Code.Backend.Domain.MFResponse import Response
from Code.Backend.Domain.DomainDataObjects.ProductPurchaseRequest import ProductPurchaseRequest
from Code.Backend.Domain.ShoppingBasket import ShoppingBasket
from Code.Backend.Domain.Store import Store
from Code.Backend.Domain.StoreOfficials.Permissions import Actions, Permissions


def search_filter(res, filterType, filterValue=None):
    # TODO think about implementation
    # 1 = price range should get filterValue as {min:x, max:y}
    if filterType == 1:
        return list(filter(lambda product: product))


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
            if products is None:
                res["products"] = []
            else:
                res["products"] = list(map(lambda x: x.get_ID(), products))
            return Response(value=res)
        except ValueError as e:
            return Response(msg=e.args[0])

    def get_stores_info(self):
        stores = list(self.stores.values())
        if not stores:
            return Response(msg="No stores in the System")
        res = []
        for store in stores:
            store_info_with_products = store.get_store_info().__dict__
            products = store.get_all_products()
            store_info_with_products["products"] = list(map(lambda x: x.get_ID(), products))
            res.append(store_info_with_products)
        return Response(value=res)

    def get_officials_stores(self, official_id):
        res = {}
        for id, store in self.stores.items():
            if official_id in store.get_officials().keys():
                res[id] = store.get_store_info().store_name
        return Response(value=res)

    def search_product(self, text, by_name, by_category, filter_type,
                       filter_value):  # TODO think about filter_value
        res = []
        for store in self.stores.values():
            tmp_store_products = store.get_all_products()
            for product in tmp_store_products:
                if by_category:
                    if text in product.get_category():
                        res.append(product)
                elif by_name:
                    if text in product.get_name():
                        res.append(product)
        if filter_type is not None:
            if filter_value is None:
                res = search_filter(res, filter_type)
            else:
                res = search_filter(res, filter_type, filter_value)
        return Response(value=res)

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
        store_id = self.__generate_id()
        newStore = Store(user_id, store_name, store_id)
        self.stores[store_id] = newStore
        return Response(value=store_id)

    def add_products_to_inventory(self, user_id: str, store_id: str, product_id: str, quantity: int):
        # check if number is not negative
        if quantity < 0:
            return Response(msg="Quantity cant be a negative number")
        try:
            store = self.__get_store(store_id)

            # check if user has access to this action
            if not store.has_access(user_id, Actions.INVENTORY_ACTION):
                return Response(msg="User does not have access to this action")

            # check if the product exists. if it is, add new quantity
            product = store.get_product(product_id, 0)
            store.update_quantities(product_id, quantity)
            return Response(value="Added " + str(quantity) + " items of " + product.get_name())
        except ValueError as e:
            return Response(msg=e.args[0])

    ##########################################
    # new function in version 2
    def add_new_product_to_inventory(self, user_id: str, store_id: str,
                                     product_name: str, product_description
                                     , price: int, category: str):
        try:
            store = self.__get_store(store_id)
            # check if user has access to this action
            if not store.has_access(user_id, Actions.INVENTORY_ACTION):
                return Response(msg="User does not have access to this action")

            ID = store.add_new_product(product_name, product_description, price, category)
            return Response(value=ID)

        except ValueError as e:
            return Response(msg=e.args[0])

    def remove_products_from_inventory(self, user_id: str, store_id: str, product_id: str, quantity: int):
        # check if number is not negative
        if quantity < 0:
            return Response(msg="Quantity cant be a negative number")
        try:

            store = self.__get_store(store_id)

            # check if user has access to this action
            if not store.has_access(user_id, Actions.INVENTORY_ACTION):
                return Response(msg="User does not have access to this action")

            # check if product exists
            product = store.get_product(product_id, quantity)

            # check if there is enough products to remove
            if product is None:
                return Response(msg="Attempt to remove more Items then the existing quantity")
            else:
                store.update_quantities(product_id, -quantity)
                return Response(value="Removed " + str(quantity) + " items of " + product.get_name())

        except ValueError as e:
            return Response(msg=e.args[0])

    def edit_product_info(self, user_id, store_id, product_id, name, description, rating
                          , price, category):
        try:
            store = self.__get_store(store_id)

            # check if user has access to this action
            if not store.has_access(user_id, Actions.INVENTORY_ACTION):
                return Response(msg="User does not have access to this action")

            # check if product exists
            product = store.get_product(product_id, 0)
            if product is None:
                return Response(msg="Product does not exists")
            else:
                store.edit_product(product_id, name, description, rating
                                   , price, category)
                return Response(value="Product was edited")

        except ValueError as e:
            return Response(msg=e.args[0])

    def add_store_owner(self, user_id: str, store_id: str, new_owner_id: str):
        try:
            store = self.__get_store(store_id)

            # check if user has access to this action
            if not store.has_access(user_id, Actions.ADD_STORE_OWNER):
                return Response(msg="User does not have access to this action")

            # check if user is already an owner or store manager
            if not store.add_owner(user_id, new_owner_id):
                return Response(msg="User is already an Owner of this store")
            return Response(value="Made User with id: " + str(user_id) + " an owner")
        except ValueError as e:
            return Response(msg=e.args[0])

    def add_store_manager(self, user_id: str, store_id: str, new_manager_id: str):
        try:
            store = self.__get_store(store_id)

            # check if user has access to this action
            if not store.has_access(user_id, Actions.ADD_STORE_MANAGER):
                return Response(msg="User does not have access to this action")

            # check if user is already a manager or store owner
            if not store.add_manager(user_id, new_manager_id):
                return Response(msg="User is already an Owner of this store")
            return Response(value="Made User with id: " + str(user_id) + " a manager")
        except ValueError as e:
            return Response(msg=e.args[0])

    def change_manager_permission(self, user_id: str, store_id: str, manager_id: str, new_permission: Dict):
        try:
            store = self.__get_store(store_id)

            # check if user has access to this action
            if not store.has_access(user_id, Actions.CHANGE_MANAGER_PERMISSION):
                return Response(msg="User does not have access to this action")

            store.change_permissions(manager_id, new_permission)
            return Response(value="Permissions successfully changed")
        except ValueError as e:
            return Response(msg=e.args[0])

    def close_store(self, user_id: str, store_id: str):
        try:
            store = self.__get_store(store_id)
            # check if user has access to this action
            if not store.has_access(user_id, Actions.CLOSE_STORE):
                return Response(msg="User does not have access to this action")

            # close store
            self.inactive_stores[store_id] = store
            self.stores.pop(store_id)
            return Response(value="Store was successfully closed")

        except ValueError as e:
            return Response(msg=e.args[0])

    def reopen_store(self, user_id: str, store_id: str):
        pass

    def get_store_roles(self, user_id: str, store_id: str):
        try:
            store = self.__get_store(store_id)

            # check if user has access to this action
            if not store.has_access(user_id, Actions.GET_STORE_ROLES):
                return Response(msg="User does not have access to this action")

            return Response(value=store.get_officials())
        except ValueError as e:
            return Response(msg=e.args[0])

    def get_users_messages(self, user_id: str, store_id: str):
        pass

    def reply_users_messages(self, user_id: str, store_id: str, user_contact_info, owner_contact_info):
        pass

    def get_store_purchase_history(self, user_id: str, store_id: str, is_admin=False):
        try:
            store = self.__get_store(store_id)

            if not store.has_access(user_id, Actions.GET_STORE_PURCHASE_HISTORY) or not is_admin:
                return Response(msg="User does not have access to this action")

            return Response(value=store.get_purchase_history())

        except ValueError as e:
            return Response(msg=e.args[0])

    def get_product(self, store_id, product_id, quantity):
        """
        checks if the product is available, and returns its reference.
        return None if not available or not exists.
        """
        store = self.__get_store(store_id)
        try:
            res = store.get_product(product_id, quantity)
            return res
        except ValueError:  # as e:
            return None  # Response(msg=e.args[0])

    def create_product_purchase_request(self, store_id, product_id, quantity):
        try:
            product = self.get_product(store_id, product_id, quantity)
            if product:
                return Response(ProductPurchaseRequest(store_id, product_id, quantity))
            return Response.from_error("Got None from get_product")
        except ValueError as e:
            return Response(msg=e.args[0])

    # TODO change store id should be in basket
    def get_basket_price(self, store_id, basket: ShoppingBasket, invisible_codes=None):
        try:
            store = self.__get_store(store_id)
            quantity_dic = basket.get_products_and_quantities()
            products_list_ids = list(quantity_dic.keys())
            product_list = list(map(lambda x: store.get_product(x, 0), products_list_ids))
            # TODO should send basket.user_state instead of None
            price = store.get_discount_policy().calculate_basket(product_list, None, quantity_dic)
            return Response(value=price)
        except ValueError as e:
            return Response(msg=e.args[0])

    def add_visible_discount(self, store_id, list_of_products_ids, discount_price, end_date):
        try:
            store = self.__get_store(store_id)
            discount = store.get_discount_policy().add_visible_discount(list_of_products_ids,
                                                                        discount_price, end_date)
            return Response(value=discount)
        except ValueError as e:
            return Response(msg=e.args[0])

    def add_conditional_discount(self, store_id, list_of_products_ids, discount_price, end_date,
                                 dic_of_products_and_quantity, min_price_for_discount):
        try:
            store = self.__get_store(store_id)
            discount = store.get_discount_policy().add_conditional_discount(list_of_products_ids, discount_price,
                                                                            end_date, dic_of_products_and_quantity,
                                                                            min_price_for_discount)
            return Response(value=discount)
        except ValueError as e:
            return Response(msg=e.args[0])

    def add_or_discount(self, store_id, first_discount, second_discount):
        try:
            store = self.__get_store(store_id)
            discount = store.get_discount_policy().add_or_discount(first_discount, second_discount)

            return Response(value=discount)
        except ValueError as e:
            return Response(msg=e.args[0])

    # ---------------------------------------------------------------------

    def __get_store(self, store_id):
        """
        check if stores exists and return it
        throws ValueError if not exist
        """
        if store_id not in self.stores:
            raise ValueError("Store id does not exist or is inactive")
        else:
            return self.stores[store_id]

    def __generate_id(self):
        self.id_counter += 1
        return str(self.id_counter)
