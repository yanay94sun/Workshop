from typing import Dict, List

from Code.Backend.Domain.DM_product_info import DM_product_info
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
        self.user_controller = None
        self.market = None
        self.store_controller = None

    """Functional requirements"""

    def initial_system(self, admin_id: str = None, admin_pwd: str = None,
                       payment_service: int = 0, supply_service: int = 0):
        """
        I.1
        -   contacts to the related services, by init the fields in the market from a fixed list of services
        -   creates the main admin, if not exist
        :return: None
        """
        self.market = Market(admin_id, admin_pwd, payment_service, supply_service)
        self.user_controller = UserController()
        self.store_controller = StoreController()
        pass

    def contact_payment_service(self, payment_info: Payment_info) -> Response:
        """
        I.3
        a payment transaction with the current payment service, with the given payment information.
        :param payment_info: the data the payment service needs to successfully manage the payment.
        :return: Response object
        """
        return Response(self.market.contact_payment_service(payment_info))
        pass

    def contact_supply_service(self, package_info: Package_info) -> Response:
        """
        I.4
        a request for a delivery from the supply service.
        :param package_info: the data the current supply service needs to successfully process the request.
        :return:
        """
        return Response(self.market.contact_supply_service(package_info))
        pass

    """
    Users requirements
    General guest actions
    """

    def enter_as_guest(self) -> Response:
        """
        II.1.1
        generates a temp id and creates a Visitor object with a default guest state and a shopping cart.
        :return:
        """
        return Response(self.user_controller.create_guest())
        # write to log

    def exit(self, user_id: str):
        """
        II.1.2
        when a guest is exit, all its data is dismissed including its shopping cart.
        :param user_id:
        :return:
        """
        return Response(self.user_controller.exit(user_id))
        pass

    def register(self, guest_id: str, user_info):
        """
        II.1.3
        register a user to the market, creates a member state.
        :param guest_id:
        :param user_info: all info needed for registration.
        :return:
        """
        return Response(self.user_controller.register(guest_id, user_info))
        pass

    def login(self, guest_id: str, username: str, password: str):
        """
        II.1.4
        changes state to logged in
        :param guest_id:
        :param username:
        :param password:
        :return:
        """
        return Response(self.user_controller.login(guest_id, username, password))
        pass

    """Guest's Purchase actions"""

    def get_store_info(self, user_id: str, store_id: str) -> Response:
        """
        II.2.1.1
        when a user request for a specific store info.
        :param user_id:
        :param store_id:
        :return: Store's info which contains:
        store's name, store's owners, rank, products
        """
        return Response(self.store_controller.get_store_info(store_id))

    def get_stores_info(self, user_id: str) -> Response:
        """
        II.2.1.2
        when a user request for all stores info.
        :param user_id:
        :return: List of store info
        """
        return Response(self.store_controller.get_stores_info())
        pass

    def search_product(self, user_id: str, product_filters: Product_search_filters):
        """
        II.2.2
        TODO add arguments
        Search a product by given product name, category or key words.
        Filtering results by given feature filters
        :param user_id:
        :param product_filters: An object contains filtering criteria, like price range, product's grade...
        :return:
        """
        return Response(self.store_controller.search_product())
        pass

    def add_product_to_shop_cart(self, user_id: str, store_id, product_id, quantity):
        """
        II.2.3
        Checks if the product is available in the store, and adds the given product to the user's shop cart.
        :param user_id:
        :param store_id:
        :param product_id:
        :param quantity:
        :return:
        """
        product_info = self.store_controller.get_product(store_id, product_id, quantity)
        # check if not None
        return Response(self.user_controller.add_product_to_shop_cart(user_id, product_info, quantity))
        pass

    def get_shop_cart(self, user_id: str) -> Response:
        """
        II.2.4
        return he information of the user shopping cart.
        :param user_id:
        :return: Shopping cart object
        """
        return Response(self.user_controller.get_shop_cart(user_id))

    def remove_product_from_shop_cart(self, user_id: str, product_id: str):
        """
        II.2.4

        :param user_id:
        :param product_id:
        :return:
        """
        return Response(self.user_controller.remove_product_from_shop_cart(user_id, product_id))

    def purchase_shop_cart(self, user_id: str):
        """
        II.2.5
        gets user's shopping cart and applies discount policies on each basket, then decrease the quantity of the
        product
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
    """Admin Section"""

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
