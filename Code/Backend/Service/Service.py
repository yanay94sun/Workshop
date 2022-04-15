from typing import Dict

from Code.Backend.Domain.Market import Market
from Code.Backend.Domain.StoreController import StoreController
from Code.Backend.Domain.UserController import UserController
from Code.Backend.Service.Objects import Shopcart_info
from Code.Backend.Service.Objects.Contact_info import Contact_info
from Code.Backend.Service.Objects.DiscountPolicy import DiscountPolicy
from Code.Backend.Service.Objects.Package_info import Package_info
from Code.Backend.Service.Objects.Payment_info import Payment_info
from Code.Backend.Service.Objects.Permissions import Permission
from Code.Backend.Service.Objects.Personal_info import Personal_info
from Code.Backend.Service.Objects.Personal_purchase_history import Personal_purchase_history
from Code.Backend.Service.Objects.Product_info import Product_info
from Code.Backend.Service.Objects.Product_search_filters import Product_search_filters
from Code.Backend.Service.Objects.PurchasePolicy import PurchasePolicy
from Code.Backend.Service.Response import Response
from Code.Backend.Service.Objects.Store_info import Store_info


class Service:
    def __init__(self):
        self.uc = UserController()
        self.market = Market()
        self.sc = StoreController()

    """Functional requirements"""

    def initial_system(self):
        """
        I.1
        :return:
        """
        pass

    def contact_payment_service(self, payment_info: Payment_info) -> Response:
        """
        I.3
        :param payment_info:
        :return: Response object
        """
        pass

    def contact_supply_service(self, package_info: Package_info) -> Response:
        """
        I.4
        :param package_info:
        :return:
        """
        pass

    """
    Users requirements
    General guest actions
    """

    def enter_as_guest(self) -> str:
        """
        II.1.1
        :return:
        """
        response = Response(self.uc.create_guest())
        # write to log
        return response.value

    def exit(self, user_id: str):
        """
        II.1.2
        :param user_id:
        :return:
        """
        pass

    def register(self, guest_id: str, user_info):
        """
        II.1.3

        :param guest_id:
        :param user_info:
        :return:
        """
        pass

    def login(self, guest_id: str, username: str, password: str):
        """
        II.1.4

        :param guest_id:
        :param username:
        :param password:
        :return:
        """
        pass

    """Guest's Purchase actions"""

    def get_store_info(self, user_id: str, store_id: str) -> Store_info:
        """
        II.2.1

        :param user_id:
        :param store_id:
        :return:
        """
        pass

    def search_product(self, user_id: str, product_filters: Product_search_filters):
        """
        II.2.2
        Search a product by given product name, category or key words.
        Filtering results by given feature filters
        :param user_id:
        :param product_filters: An object contains filtering criteria, like price range, product's grade...
        :return:
        """

        pass

    def add_product_to_shop_cart(self, user_id: str, product_info: Product_info):
        """
        II.2.3

        :param user_id:
        :param product_info:
        :return:
        """
        pass

    def get_shop_cart(self, user_id: str) -> Shopcart_info:
        """
        II.2.4

        :param user_id:
        :return:
        """

    def remove_product_from_shop_cart(self, user_id: str, product_id: str):
        """
        II.2.4

        :param user_id:
        :param product_id:
        :return:
        """

    def purchase_shop_cart(self, user_id: str):
        """
        II.2.5

        :param user_id:
        :return:
        """
        pass

    """Member's purchase actions"""

    def logout(self, user_id: str):
        """
        II.3.1
        Logging out, the shopping cart is saved.
        :param user_id:
        :return:
        """
        pass

    def open_store(self, user_id: str):
        """
        II.3.2
        TODO should receive more arguments
        A registered member may open a store and be the founder and a manager.
        :param user_id:
        :return:
        """
        pass

    def review_product(self, user_id: str, product_info, review: str):
        """
        II.3.3
        Nitzan: put the responsibility in the user

        :param user_id:
        :param product_info
        :param review:
        :return:
        """
        pass

    def grade_product(self, user_id: str, product_info: str, grade):
        """
        Nitzan: put the responsibility in the user

        II.3.4.1
        :param user_id:
        :param product_info:
        :param grade:
        :return:
        """
        pass

    def grade_store(self, user_id: str, store_id: str, grade):
        """
        TODO
        II.3.4.2
        :param user_id:
        :param store_id:
        :param grade:
        :return:
        """
        pass

    def contact_store(self, user_id: str, store_id: str, contact_info: Contact_info):
        """
        Nitzan: put the responsibility in the store
        II.3.5

        :param user_id:
        :param store_id:
        :param contact_info:
        :return:
        """
        pass

    def complaint(self, user_id: str, comp: Contact_info):
        """
        Nitzan: put the responsibility in the market
        II.3.6

        :param user_id:
        :param comp:
        :return:
        """
        pass

    def get_personal_purchase_history(self, user_id: str) -> Personal_purchase_history:
        """
        Nitzan: put the responsibility in the user
        II.3.7

        :param user_id:
        :return:
        """
        pass

    def get_personal_info(self, user_id: str) -> Personal_info:
        """
        Nitzan: put the responsibility in the user
        II.3.8

        :param user_id:
        :return:
        """
        pass

    def edit_personal_info(self, user_id: str, new_personal_info: Personal_info):
        """
        Nitzan: put the responsibility in the user
        II.3.8

        :param user_id:
        :param new_personal_info:
        :return:
        """
        pass

    def upgrade_member_security(self, user_id: str):
        """
        II.3.9
        TODO more arguments might be necessary + give a controller responsibility
        :param user_id:
        :return:
        """
        pass

    # def add_products_to_inventory(self, user_id: str, store_id: str, products: dict):
    #     """
    #     II.4.1
    #
    #     :param user_id:
    #     :param store_id:
    #     :param products: {product_info: Product_info, quantity:int}
    #     :return:
    #     """
    #     pass
    #
    # def remove_products_to_inventory(self, user_id: str, store_id: str, products: dict):
    #
    def manage_inventory(self, user_id: str, store_id: str, products: Dict[Product_info, int]):
        """
        II.4.1
        TODO: maybe to split this into 3 funcs??? + decide whose responsible
        add, remove and edit the inventory
        :param user_id:
        :param store_id:
        :param products: {product_info: Product_info, quantity:int}
        :return:
        """
        pass

    def edit_store_policy(self, user_id: str, store_id: str):
        """
        II.4.2
        *NOT*  need to implement to this version
        :param user_id:
        :param store_id:
        :return:
        """
        pass

    def change_purchase_policy(self, user_id: str, store_id: str, purchase_policy: PurchasePolicy):
        """
        II.4.3.1
        :param user_id:
        :param store_id:
        :param purchase_policy:
        :return:
        """
        pass

    def change_discount_policy(self, user_id: str, store_id: str, discount_policy: DiscountPolicy):
        """
        II.4.3.2
        :param user_id:
        :param store_id:
        :param discount_policy:
        :return:
        """
        pass

    """ Nitzan: put responsibilities the next methods in Store Controller, until II.4.12.2"""

    def add_store_owner(self, user_id: str, store_id: str, new_owner_id: str):
        """
        II.4.4
        :param user_id:
        :param store_id:
        :param new_owner_id:
        :return:
        """
        pass

    def remove_store_owner(self, user_id: str, store_id: str, owner_id: str):
        """
        II.4.5
        :param user_id:
        :param store_id:
        :param owner_id:
        :return:
        """
        pass

    def add_store_manager(self, user_id: str, store_id: str, new_manager_id: str):
        """
        II.4.6
        :param user_id:
        :param store_id:
        :param new_manager_id:
        :return:
        """
        pass

    def change_manager_permission(self, user_id: str, store_id: str, manager_id: str, new_permission: Permission):
        """
        II.4.7
        :param user_id:
        :param store_id:
        :param manager_id:
        :param new_permission:
        :return:
        """
        pass

    def remove_store_manager(self, user_id: str, store_id: str, manager_id: str):
        """
        II.4.8
        :param user_id:
        :param store_id:
        :param manager_id:
        :return:
        """
        pass

    def close_store(self, user_id: str, store_id: str):
        """
        II.4.9
        :param user_id:
        :param store_id:
        :return:
        """
        pass

    def reopen_store(self, user_id: str, store_id: str):
        """
        II.4.10
        :param user_id:
        :param store_id:
        :return:
        """
        pass

    def get_store_roles(self, user_id: str, store_id: str):
        """
        II.4.11
        :param user_id:
        :param store_id:
        :return:
        """
        pass

    def get_users_messages(self, user_id: str, store_id: str):
        """
        II.4.12.1
        :param user_id:
        :param store_id:
        :return:
        """
        pass

    def reply_users_messages(self, user_id: str, store_id: str, user_contact_info: Contact_info,
                             owner_contact_info: Contact_info):
        """
        II.4.12.2
        :param user_id:
        :param store_id:
        :param user_contact_info:
        :param owner_contact_info:
        :return:
        """
        pass

    def get_store_purchase_history(self, user_id: str, store_id: str):
        """
        II.4.13
        :param user_id:
        :param store_id:
        :return:
        """
        pass

    """ Nitzan: put responsibilities of the following methods in Market """

    def close_store_permanently(self, user_id: str, store_id: str):
        """
        II.6.1
        :param user_id:
        :param store_id:
        :return:
        """
        pass

    def remove_member(self, user_id: str, member_id: str):
        """
        II.6.2
        :param user_id:
        :param member_id:
        :return:
        """
        pass

    def get_all_users_messages_by_admin(self, user_id: str):
        """
        II.6.3.1
        :param user_id:
        :return:
        """
        pass

    def reply_users_messages_by_admin(self, user_id: str, store_id: str, user_contact_info: Contact_info,
                                      admin_contact_info: Contact_info):
        """
        II.6.3.2
        :param user_id:
        :param store_id:
        :param user_contact_info:
        :param admin_contact_info:
        :return:
        """
        pass

    def get_stores_purchase_history_by_admin(self, user_id: str, store_id=None):
        """
        II.6.4
        :param user_id:
        :param store_id:
        :return:
        """
        pass

    def get_system_statistic_by_admin(self, user_id: str):
        """
        II.6.5
        :param user_id:
        :return:
        """
        pass
