from typing import Dict, List

from Code.Backend.Domain.DiscountPolicyObjects.DiscountPolicy import DiscountPolicy
from Code.Backend.Domain.DomainDataObjects.ProductPurchaseRequest import ProductPurchaseRequest
from Code.Backend.Domain.StoreOfficials.Permissions import Permissions, Actions
from Code.Backend.Domain.Product import Product
from Code.Backend.Domain.Purchase import Purchase
from Code.Backend.Domain.PurchasePolicyObjects.PurchasePolicy import PurchasePolicy
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
        self.__id_counter = 0

    def get_store_info(self):
        return self.__store_info

    def get_store_officials(self):
        return self.__officials

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

    def add_new_product(self, name, description, price, category):
        if name in map(lambda x: x.get_name(), list(self.__products.values())):
            raise ValueError("product name already exist")
        self.__id_counter += 1
        ID = str(self.__id_counter)
        self.__products[ID] = Product(ID, name, description, price, category, self.__store_info.ID)
        self.__quantities[ID] = 0
        return ID

    def edit_product(self, product_id, name, description, rating, price, category):
        product = self.__products[product_id]
        if name is not None and name != "":
            product.change_name(name)
        if description is not None and description != "":
            product.change_description(description)
        if rating is not None and rating != -1:
            product.change_rating(rating)
        if price is not None and price != -1:
            product.change_price(price)
        if category is not None and category != "":
            product.change_category(category)

    def add_owner(self, user_id: str, new_user_id: str):
        if new_user_id in self.__officials.keys():
            return False

        self.__officials[new_user_id] = StoreOwner(new_user_id, self.__officials[user_id])
        return True

    def add_manager(self, user_id: str, new_manager_id: str):
        if new_manager_id in self.__officials.keys():
            return False
        self.__officials[new_manager_id] = StoreManager(new_manager_id,
                                                        self.__officials[user_id])
        return True

    def change_permissions(self, user_id, new_permission):
        self.__officials[user_id].set_permission(new_permission)

    def get_officials(self):
        return self.__officials

    def add_purchase_to_history(self, product_name, deal_price, quantity):
        self.__purchase_history.append(Purchase(product_name, deal_price, quantity))

    def get_purchase_history(self):
        return self.__purchase_history

    def get_discount_policy(self):
        return self.__discount_policy

    def remove_store_owner_end_his_children_and_his_children_s_children_and_his_family_and_kill_them(self,
                                                                                                     remover_username,
                                                                                                     subject_username):
        if remover_username not in self.__officials:
            raise Exception("isn't official")
        if isinstance(self.__officials[remover_username], StoreManager):
            raise Exception("isn't store owner or founder")
        if subject_username not in self.__officials:
            raise Exception("subject isn't official")
        if self.__officials[subject_username].appointee.appointed != remover_username:
            raise Exception("subject wasn't appointed by remover")
        self.remove_store_owner_end_his_children_and_his_children_s_children_and_his_family_and_kill_them_rec_helper(
            subject_username
        )

    def remove_store_owner_end_his_children_and_his_children_s_children_and_his_family_and_kill_them_rec_helper(self,
                                                                                                                subject_username):
        all_my_children = list(filter(lambda official:
                                      official.appointee and
                                      official.appointee.appointed == subject_username,
                                      self.__officials.values()))
        for child in all_my_children:
            self.remove_store_owner_end_his_children_and_his_children_s_children_and_his_family_and_kill_them_rec_helper(
                child.appointed)
        self.__officials.pop(subject_username)

    def remove_products_by_id(self, product_id, quantity):
        if product_id in self.__products:
            if self.__quantities[product_id] >= quantity:
                self.__quantities[product_id] -= quantity

    def has_quantity(self, product_id, quantity):
        if product_id in self.__products:
            return self.__quantities[product_id] >= quantity
        raise BufferError("store does not exist")

    def purchase_single_product(self, ppr: ProductPurchaseRequest):
        if ppr.product_id not in self.__products:
            raise Exception(f"product {ppr.product_id} doesnt appear in store {ppr.store_id}")
        with self.__products[ppr.product_id]:
            if self.has_quantity(ppr.product_id, ppr.quantity):
                self.remove_products_by_id(ppr.product_id, ppr.quantity)
            else:
                raise Exception(f"quantity of {ppr.product_id} is not enough")

    def revert_purchase_single_product(self, ppr):
        with self.__products[ppr.product_id]:
            self.__quantities[ppr.product_id] += ppr.quantity

    def get_purchase_policy(self):
        return self.__purchase_policy

    def get_product_and_quantities(self, product_id):
        if product_id in self.__products.keys():
            return {"product": self.__products[product_id].__dict__, "quantity": self.__quantities[product_id]}
        else:
            raise ValueError("no object with this id on this store")

    def create_store_from_db(self, products, discount_policy, purchase_policy, officials
                             , purchase_history, id_counter):
        self.__products = {x.product_id: self.__create_product_from_db(x) for x in products}
        self.__quantities = {x.product_id: x.quantity for x in products}
        self.__discount_policy = discount_policy
        self.__purchase_policy = purchase_policy
        self.__officials: Dict[str, StoreOfficial] = self.__create_officials_from_db(officials)
        self.__purchase_history = purchase_history
        self.__id_counter = id_counter

    def __create_product_from_db(self, productDB):
        # TODO Nitzan product id
        product = Product(productDB.product_id, productDB.name, productDB.description,
                          productDB.price, productDB.category, productDB, productDB.store_id)
        product.change_rating(productDB.rating)
        return product

    def __create_officials_from_db(self, officialsDB):
        officials = {}
        founderDB = next(filter(lambda x: not x.appointee, officialsDB))
        currentOfficial = StoreFounder(founderDB.username)
        officials[founderDB.username] = currentOfficial
        self.officialRec(currentOfficial, officialsDB, officials)
        return officials


    def officialRec(self, curr, officialsDB, officials):
            next_in_line = list(filter(lambda x: x.appointee == curr.appointed, officialsDB))
            if not next_in_line:
                return
            for officialSon in next_in_line:
                if officialSon.is_owner:
                    currentOfficial = StoreOwner(officialSon.username, curr)
                else:
                    currentOfficial = StoreManager(officialSon.username, curr)
                currentOfficial.set_permission(Permissions({
                                        Actions.INVENTORY_ACTION.value: officialSon.INVENTORY_ACTION,
                                        Actions.CHANGE_MANAGER_PERMISSION.value: officialSon.CHANGE_MANAGER_PERMISSION,
                                        Actions.ADD_STORE_MANAGER.value: officialSon.ADD_STORE_MANAGER,
                                        Actions.ADD_STORE_OWNER.value: officialSon.ADD_STORE_OWNER,
                                        Actions.GET_STORE_PURCHASE_HISTORY.value: officialSon.GET_STORE_PURCHASE_HISTORY,
                                        Actions.CLOSE_STORE.value: officialSon.CLOSE_STORE,
                                        Actions.GET_STORE_ROLES.value: officialSon.GET_STORE_ROLES,
                                        Actions.DISCOUNT_MANAGEMENT: officialSon.PURCHASE_MANAGEMENT,
                                        Actions.PURCHASE_MANAGEMENT: officialSon.DISCOUNT_MANAGEMENT}))
                officials[currentOfficial.appointee] = currentOfficial
                self.officialRec(currentOfficial, officialsDB, officials)

