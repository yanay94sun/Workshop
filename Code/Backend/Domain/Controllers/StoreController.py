from typing import Dict, Iterable, List

from Code.Backend.Domain.DiscountPolicyObjects.DiscountPolicy import DiscountPolicy
from Code.Backend.Domain.MFResponse import Response
from Code.Backend.Domain.DomainDataObjects.ProductPurchaseRequest import ProductPurchaseRequest
from Code.Backend.Domain.PurchasePolicyObjects.PurchasePolicy import PurchasePolicy
from Code.DAL.Objects.store import PurchasePolicy as PurchasePolicyDB, Official
from Code.DAL.Objects.store import DiscountPolicy as DiscountPolicyDB
from Code.Backend.Domain.ShoppingBasket import ShoppingBasket
from Code.Backend.Domain.Store import Store
from Code.Backend.Domain.StoreOfficials.Permissions import Actions
# import Code.DAL.main as dal
# from Code.DAL.Objects.store import StoreBase


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
                res["products"] = list(map(lambda x: x.__dict__, products))
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
        # TODO think about it should we call all the stores in data base?
        """
        returns dic {store id: store name}
        """
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
        if filter_type:
            if filter_value:
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

        # add to db
        # store_base = StoreBase(store_id=store_id, is_active=True, name=store_name, founder_username=user_id
        #                        , id_counter=0)
        # # TODO purchasePolicy = PurchasePolicyDB()
        # discount_policy = DiscountPolicyDB(store_id=store_id, id_counter=0, discounts=[])
        # founderDb = Official(username=user_id, appointee=None, INVENTORY_ACTION=True,
        #                      CHANGE_MANAGER_PERMISSION=True,
        #                      ADD_STORE_MANAGER=True,
        #                      ADD_STORE_OWNER=True,
        #                      GET_STORE_PURCHASE_HISTORY=True,
        #                      CLOSE_STORE=True,
        #                      GET_STORE_ROLES=True,
        #                      PURCHASE_MANAGEMENT=True,
        #                      DISCOUNT_MANAGEMENT=True,
        #                      is_owner=True
        #                      )
        # dal.persist_store(store_base, purchase_policy, discount_policy, [], [founderDb])
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
            return Response(value="Made User with id: " + str(new_owner_id) + " an owner")
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
                return Response(msg="User is already a Manager of this store")
            return Response(value="Made User with id: " + str(new_manager_id) + " a manager")
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

    def add_visible_discount_by_product(self, user_id, store_id,
                                        discount_price, end_date, product_id):
        """
        """
        try:
            store = self.__get_store(store_id)

            # check if user has access to this action
            if not store.has_access(user_id, Actions.DISCOUNT_MANAGEMENT):
                return Response(msg="User does not have access to this action")

            discount = store.get_discount_policy(). \
                add_visible_discount(discount_price, end_date, product_id, 1)
            return Response(value=discount)
        except ValueError as e:
            return Response(msg=e.args[0])

    def add_visible_discount_by_category(self, user_id, store_id,
                                         discount_price, end_date, category_name):
        """
        """
        try:
            store = self.__get_store(store_id)

            # check if user has access to this action
            if not store.has_access(user_id, Actions.DISCOUNT_MANAGEMENT):
                return Response(msg="User does not have access to this action")

            discount = store.get_discount_policy(). \
                add_visible_discount(discount_price, end_date, category_name, 2)
            return Response(value=discount)
        except ValueError as e:
            return Response(msg=e.args[0])

    def add_visible_discount_by_store(self, user_id, store_id,
                                      discount_price, end_date):
        """
        """
        try:
            store = self.__get_store(store_id)

            # check if user has access to this action
            if not store.has_access(user_id, Actions.DISCOUNT_MANAGEMENT):
                return Response(msg="User does not have access to this action")

            discount = store.get_discount_policy(). \
                add_visible_discount(discount_price, end_date, "", 3)
            return Response(value=discount)
        except ValueError as e:
            return Response(msg=e.args[0])

    def add_conditional_discount_by_product(self, user_id, store_id, discount_price, end_date, product_id,
                                            dic_of_products_and_quantity, min_price_for_discount):
        """
       add to dic_of_products_and_quantity if the condition is "at least x of product y" {id:quantity}
       add to min_price_to_have_for_purchase if the condition is "at least x of total cart price"
        """
        try:
            store = self.__get_store(store_id)

            # check if user has access to this action
            if not store.has_access(user_id, Actions.DISCOUNT_MANAGEMENT):
                return Response(msg="User does not have access to this action")

            discount = store.get_discount_policy().add_conditional_discount(discount_price,
                                                                            end_date, product_id, 1,
                                                                            dic_of_products_and_quantity,
                                                                            min_price_for_discount)
            return Response(value=discount)
        except ValueError as e:
            return Response(msg=e.args[0])

    def add_conditional_discount_by_category(self, user_id, store_id, discount_price, end_date, category_name,
                                             dic_of_products_and_quantity, min_price_for_discount):
        """
       add to dic_of_products_and_quantity if the condition is "at least x of product y" {id:quantity}
       add to min_price_to_have_for_purchase if the condition is "at least x of total cart price"
        """
        try:
            store = self.__get_store(store_id)

            # check if user has access to this action
            if not store.has_access(user_id, Actions.DISCOUNT_MANAGEMENT):
                return Response(msg="User does not have access to this action")

            discount = store.get_discount_policy().add_conditional_discount(discount_price,
                                                                            end_date, category_name, 2,
                                                                            dic_of_products_and_quantity,
                                                                            min_price_for_discount)
            return Response(value=discount)
        except ValueError as e:
            return Response(msg=e.args[0])

    def add_conditional_discount_by_store(self, user_id, store_id, discount_price, end_date,
                                          dic_of_products_and_quantity, min_price_for_discount):
        """
       add to dic_of_products_and_quantity if the condition is "at least x of product y" {id:quantity}
       add to min_price_to_have_for_purchase if the condition is "at least x of total cart price"
        """
        try:
            store = self.__get_store(store_id)

            # check if user has access to this action
            if not store.has_access(user_id, Actions.DISCOUNT_MANAGEMENT):
                return Response(msg="User does not have access to this action")

            discount = store.get_discount_policy().add_conditional_discount(discount_price,
                                                                            end_date, "", 3,
                                                                            dic_of_products_and_quantity,
                                                                            min_price_for_discount)
            return Response(value=discount)
        except ValueError as e:
            return Response(msg=e.args[0])

    def add_or_discount(self, user_id, store_id, first_discount_id, second_discount_id):
        try:
            store = self.__get_store(store_id)

            # check if user has access to this action
            if not store.has_access(user_id, Actions.DISCOUNT_MANAGEMENT):
                return Response(msg="User does not have access to this action")

            discount = store.get_discount_policy().add_or_discount(first_discount_id, second_discount_id)

            return Response(value=discount)
        except ValueError as e:
            return Response(msg=e.args[0])

    def add_and_discount(self, user_id, store_id, first_discount_id, second_discount_id):
        try:
            store = self.__get_store(store_id)

            # check if user has access to this action
            if not store.has_access(user_id, Actions.DISCOUNT_MANAGEMENT):
                return Response(msg="User does not have access to this action")

            discount = store.get_discount_policy().add_and_discount(first_discount_id, second_discount_id)

            return Response(value=discount)
        except ValueError as e:
            return Response(msg=e.args[0])

    def add_xor_discount(self, user_id, store_id, first_discount_id, second_discount_id):
        try:
            store = self.__get_store(store_id)

            # check if user has access to this action
            if not store.has_access(user_id, Actions.DISCOUNT_MANAGEMENT):
                return Response(msg="User does not have access to this action")

            discount = store.get_discount_policy().add_xor_discount(first_discount_id, second_discount_id)

            return Response(value=discount)
        except ValueError as e:
            return Response(msg=e.args[0])

    def add_sum_discount(self, user_id, store_id, first_discount_id, second_discount_id):
        try:
            store = self.__get_store(store_id)

            # check if user has access to this action
            if not store.has_access(user_id, Actions.DISCOUNT_MANAGEMENT):
                return Response(msg="User does not have access to this action")

            discount = store.get_discount_policy().add_sum_discount(first_discount_id, second_discount_id)

            return Response(value=discount)
        except ValueError as e:
            return Response(msg=e.args[0])

    def add_max_discount(self, user_id, store_id, first_discount_id, second_discount_id):
        try:
            store = self.__get_store(store_id)

            # check if user has access to this action
            if not store.has_access(user_id, Actions.DISCOUNT_MANAGEMENT):
                return Response(msg="User does not have access to this action")

            discount = store.get_discount_policy().add_max_discount(first_discount_id, second_discount_id)

            return Response(value=discount)
        except ValueError as e:
            return Response(msg=e.args[0])

    def check_purchase_policy(self, store_id, basket: ShoppingBasket):
        """
        checks if all purchase condition are met
        """
        try:
            store = self.__get_store(store_id)
            quantity_dic = basket.get_products_and_quantities()
            products_list_ids = list(quantity_dic.keys())
            product_list = list(map(lambda x: store.get_product(x, 0), products_list_ids))
            # TODO should send basket.user_state instead of None
            can_buy = store.get_purchase_policy().can_buy(product_list, None, quantity_dic)
            return Response(value=can_buy)
        except ValueError as e:
            return Response(msg=e.args[0])

    def add_simple_purchase_rule_by_category(self, user_id, store_id, by_category):
        """
           add to products_to_have_for_purchase if the condition is "at least x of product y"
           add to min_price_to_have_for_purchase if the condition is "at least x of total cart price"
           add to by_category if the condition is "the cart should have at least one product of category x"
           by store i don't know...
           """
        try:
            store = self.__get_store(store_id)

            # check if user has access to this action
            if not store.has_access(user_id, Actions.PURCHASE_MANAGEMENT):
                return Response(msg="User does not have access to this action")

            purchase_rule = store.get_purchase_policy().add_simple_purchase_rule([], 0, by_category, None)
            return Response(value=purchase_rule)
        except ValueError as e:
            return Response(msg=e.args[0])
        # /////

    def add_simple_purchase_rule_by_product(self, user_id, store_id, products_to_have_for_purchase):
        """
           add to products_to_have_for_purchase if the condition is "at least x of product y"
           add to min_price_to_have_for_purchase if the condition is "at least x of total cart price"
           add to by_category if the condition is "the cart should have at least one product of category x"
           by store i don't know...
           """
        try:
            store = self.__get_store(store_id)

            # check if user has access to this action
            if not store.has_access(user_id, Actions.PURCHASE_MANAGEMENT):
                return Response(msg="User does not have access to this action")

            purchase_rule = store.get_purchase_policy().add_simple_purchase_rule(
                products_to_have_for_purchase, 0, "",
                None)
            return Response(value=purchase_rule)
        except ValueError as e:
            return Response(msg=e.args[0])
        # ///

    def add_simple_purchase_rule_by_min_price(self, user_id, store_id, min_price_to_have_for_purchase):
        """
           add to products_to_have_for_purchase if the condition is "at least x of product y"
           add to min_price_to_have_for_purchase if the condition is "at least x of total cart price"
           add to by_category if the condition is "the cart should have at least one product of category x"
           by store i don't know...
           """
        try:
            store = self.__get_store(store_id)

            # check if user has access to this action
            if not store.has_access(user_id, Actions.PURCHASE_MANAGEMENT):
                return Response(msg="User does not have access to this action")

            purchase_rule = store.get_purchase_policy().add_simple_purchase_rule([],
                                                                                 min_price_to_have_for_purchase, "",
                                                                                 None)
            return Response(value=purchase_rule)
        except ValueError as e:
            return Response(msg=e.args[0])

    def add_and_purchase_rule(self, user_id, store_id, first_rule_id, second_rule_id):
        try:
            store = self.__get_store(store_id)

            # check if user has access to this action
            if not store.has_access(user_id, Actions.PURCHASE_MANAGEMENT):
                return Response(msg="User does not have access to this action")

            purchase_rule = store.get_purchase_policy().add_and_purchase_rule(first_rule_id, second_rule_id)
            return Response(value=purchase_rule)
        except ValueError as e:
            return Response(msg=e.args[0])

    def add_or_purchase_rule(self, user_id, store_id, first_rule_id, second_rule_id):
        try:
            store = self.__get_store(store_id)

            # check if user has access to this action
            if not store.has_access(user_id, Actions.PURCHASE_MANAGEMENT):
                return Response(msg="User does not have access to this action")

            purchase_rule = store.get_purchase_policy().add_or_purchase_rule(first_rule_id, second_rule_id)
            return Response(value=purchase_rule)
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

    def remove_store_owner(self, remover_username, store_id, subject_username):
        return self.stores[
            store_id].remove_store_owner_end_his_children_and_his_children_s_children_and_his_family_and_kill_them(
            remover_username, subject_username)

    def __revert_purchase(self, product_to_revert: List[ProductPurchaseRequest]):
        for ppr in product_to_revert:
            self.stores[ppr.store_id].revert_purchase_single_product(ppr)

    def remove_all_products_for_purchasing(self, all_products: List[ProductPurchaseRequest]):
        # to_revert = []
        # all_products.sort(key=lambda ppr: ppr.product_id)
        # for ppr in all_products:
        #     if ppr.store_id not in self.stores:
        #         self.__revert_purchase(to_revert)
        #         return Response.from_error(f"store id {ppr.store_id} doesnt exist")
        #     single_purchase = self.stores[ppr.store_id].purchase_single_product(ppr)
        #     if single_purchase.error_occured():
        #         self.__revert_purchase(to_revert)
        #         return single_purchase
        # return Response()

        try:
            if all(map(lambda p: self.stores[p.store_id].has_quantity(p.product_id, p.quantity), all_products)):
                for p in all_products:
                    self.stores[p.product_id].remove_products_by_id(p.product_id, p.quantity)
                return Response()
        except Exception as e:
            return Response(msg=e.args[0])
        return Response(msg="some products has not enough quantity")

    def valid_all_products_for_purchase(self, all_products: List[ProductPurchaseRequest]):
        return all(map(lambda p: self.stores[p.store_id].has_quantity(p.product_id, p.quantity), all_products))

    def get_product_and_quantities(self, store_id, product_id):
        try:
            store = self.__get_store(store_id)
            return Response(value=store.get_product_and_quantities(product_id))
        except ValueError as e:
            return Response(msg=e.args[0])

    def get_permissions(self, store_id, user_id):
        try:
            store = self.__get_store(store_id)
            officials = store.get_officials()
            permissions = {}
            for key, value in officials.items():
                if key == user_id:
                    permissions[1] = value.check_permission(Actions.INVENTORY_ACTION)
                    permissions[2] = value.check_permission(Actions.ADD_STORE_OWNER)
                    permissions[3] = value.check_permission(Actions.ADD_STORE_MANAGER)
                    permissions[4] = value.check_permission(Actions.CHANGE_MANAGER_PERMISSION)
                    permissions[5] = value.check_permission(Actions.CLOSE_STORE)
                    permissions[6] = value.check_permission(Actions.GET_STORE_ROLES)
                    permissions[7] = value.check_permission(Actions.GET_STORE_PURCHASE_HISTORY)
                    permissions[8] = value.check_permission(Actions.DISCOUNT_MANAGEMENT)
                    permissions[9] = value.check_permission(Actions.PURCHASE_MANAGEMENT)
                    break
            return Response(value=permissions)

        except ValueError as e:
            return Response(msg=e.args[0])

    def get_visible_discounts(self, store_id):
        try:
            store = self.__get_store(store_id)
            return Response(value=store.get_discount_policy().get_visible_discounts())
        except ValueError as e:
            return Response(msg=e.args[0])

    def get_conditional_discounts(self, store_id):
        try:
            store = self.__get_store(store_id)
            return Response(value=store.get_discount_policy().get_conditional_discounts())
        except ValueError as e:
            return Response(msg=e.args[0])

    def get_combined_discounts(self, store_id):
        try:
            store = self.__get_store(store_id)
            return Response(value=store.get_discount_policy().get_combined_discounts())
        except ValueError as e:
            return Response(msg=e.args[0])

    # def __get_data_from_database(self):
    #     max_id = -1
    #     storesDB = dal.get_all_stores()
    #     for storeDB in storesDB:
    #         founder = storeDB.store.founder_username
    #         store_name = storeDB.store.name
    #         store_id = storeDB.store.store_id
    #         if store_id > max_id:
    #             max_id = store_id
    #         store = Store(founder, store_name, store_id)
    #
    #         store_id_counter = storeDB.store.id_counter
    #
    #         purchase_policy = PurchasePolicy()
    #         purchase_policy.create_purchase_policy_from_db(storeDB.purchase_policy.purchase_rules,
    #                                                        storeDB.purchase_policy.complex_purchase_rules,
    #                                                        storeDB.purchase_policy.id_counter)
    #
    #         discount_policy = DiscountPolicy()
    #         discount_policy.create_discount_policy_from_db(storeDB.discount_policy.discounts,
    #                                                        storeDB.discount_policy.complex_discounts
    #                                                        , storeDB.discount_policy.id_counter)
    #         # TODO store_history = storeDB.purchase_history
    #
    #         store.create_store_from_db(storeDB.products, discount_policy, purchase_policy
    #                                    , storeDB.officials, [], store_id_counter)
    #         if storeDB.store.is_active:
    #             self.stores[store_id] = store
    #         else:
    #             self.inactive_stores[store_id] = store
    #     self.id_counter = max_id + 1
