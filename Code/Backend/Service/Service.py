import threading
from typing import Dict

from Code.Backend.Domain.Controllers.Market import Market
from Code.Backend.Domain.Controllers.StoreController import StoreController
from Code.Backend.Domain.Controllers.UserController import UserController
from Code.Backend.Domain.DomainDataObjects.ProductPurchaseRequest import ProductPurchaseRequest
from Code.Backend.Service.Objects.Contact_info import Contact_info
from Code.Backend.Service.Objects.DiscountPolicy import DiscountPolicy
from Code.Backend.Service.Objects.Package_info import Package_info
from Code.Backend.Service.Objects.Payment_info import Payment_info
from Code.Backend.Service.Objects.Permissions import Permission
from Code.Backend.Service.Objects.Personal_info import Personal_info
from Code.Backend.Service.Objects.Personal_purchase_history import Personal_purchase_history
from Code.Backend.Service.Objects.Product_search_filters import Product_search_filters
from Code.Backend.Service.Objects.PurchasePolicy import PurchasePolicy
from Code.Backend.Service.Response import Response

ADMIN_ID = "-1"

class Service:
    def __init__(self):
        self.user_controller: UserController = None
        self.market: Market = None
        self.store_controller: StoreController = None
        self.purchase_lock = threading.Condition()

    """Functional requirements"""

    def initial_system(self, admin_id: str = None, admin_pwd: str = None,
                       payment_service: int = 0, supply_service: int = 0):
        """
        I.1
        -   contacts to the related services, by init the fields in the market from a fixed list of services
        -   creates the main admin, if not exist
        :param admin_id: if not None, one of the system's admins
        :param admin_pwd: if admin id is not None, is the password of the corresponds admin id
        :param payment_service: an Enum to configure the payment service
        :param supply_service: an Enum to configure the supply service
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
        return Response(self.market.contact_payment_service(self.__service_payment_info_to_domain(payment_info)))

    def __service_payment_info_to_domain(self, payment_info):
        """
        converts ...
        """
        pass

    def contact_supply_service(self, package_info: Package_info) -> Response:
        """
        I.4
        a request for a delivery from the supply service.
        :param package_info: the data the current supply service needs to successfully process the request.
        :return:
        """
        return Response(self.market.contact_supply_service(self.__service_supply_info_to_domain(package_info)))

    def __service_supply_info_to_domain(self, supply_info):
        """

        """
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

    def register(self, guest_id: str, user_info: Dict):
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

    def get_stores_info(self, user_id: str, store_id) -> Response:
        """
        II.2.1.2
        when a user request for all stores info.
        :param user_id:
        :param: store_id
        :return: List of store info
        """
        return Response(self.store_controller.get_store_info(store_id))
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
        supports only instant purchase
        :param user_id:
        :param store_id:
        :param product_id:
        :param quantity:
        :return:
        """
        prod_pur_req_response = self.store_controller.create_product_purchase_request(store_id, product_id, quantity)
        # check if not None
        if not prod_pur_req_response.error_occurred():
            return Response(self.user_controller.add_product_to_shop_cart(user_id, prod_pur_req_response.value))
        return prod_pur_req_response

    def get_shopping_cart(self, user_id: str) -> Response:
        """
        II.2.4
        return he information of the user shopping cart.
        :param user_id:
        :return: Shopping cart object
        """
        return Response(self.user_controller.get_shopping_cart(user_id))

    def remove_product_from_shopping_cart(self, user_id: str, ppr: ProductPurchaseRequest):  # TODO Basket!
        """
        II.2.4

        :param user_id:
        :param ppr:
        :return:
        """
        return Response(self.user_controller.remove_product_from_shopping_cart(user_id, ppr))

    def purchase_shopping_cart(self, user_id: str, payment_info):
        """
        II.2.5
        gets user's shopping cart and applies discount policies on each basket, then decrease the quantity of the
        product in the store
        supports only instant purchase
        :param user_id:
        :return:
        """
        with self.purchase_lock:
            cart = self.user_controller.get_shopping_cart()
            all_products = [p for p in cart.value.iter_products()]

            all_removed = self.store_controller.remove_all_products_for_purchasing(all_products)
            if all_removed.error_occured():
                return Response(all_removed)

        # pay, if error occured revert
        # revert: self.store_controller.revert_purchase_requests(all_products)

        self.store_controller.update_purchase_history(user_id, all_products)
        return Response()



    """Member's purchase actions"""

    def logout(self, user_id: str):
        """
        II.3.1
        Logging out, the shopping cart is saved.
        :param user_id:
        :return:
        """
        return Response(self.user_controller.logout(user_id))

    def open_store(self, user_id: str, store_name: str):
        """
        II.3.2
        A registered member may open a store and be the founder and a manager.
        :param user_id:
        :param store_name: the store's name
        :return:
        """
        if not self.user_controller.is_logged_in(user_id):
            return Response(msg="Not logged in")
        return Response(self.store_controller.open_store(user_id, store_name))
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

    def add_products_to_inventory(self, user_id: str, store_id: str, product_id: str, quantity: int):
        """
        II.4.1.1
        adds the given product's quantity to the store's inventory.
        if the product id does not exists, it adds a new default product info.
        (to edit to product info, user should call edit)
        :param user_id:
        :param store_id:
        :param product_id:
        :param quantity:
        :return:
        """
        if not self.user_controller.is_logged_in(user_id):
            return Response(msg="Not logged in")
        return Response(self.store_controller.add_products_to_inventory(user_id, store_id, product_id, quantity))

    def remove_products_from_inventory(self, user_id: str, store_id: str, product_id: str, quantity: int):
        """
        II.4.1.2

        :param user_id:
        :param store_id:
        :param product_id
        :param quantity:
        :return:
        """
        if not self.user_controller.is_logged_in(user_id):
            return Response(msg="Not logged in")
        return Response(self.store_controller.remove_products_from_inventory(user_id, store_id, product_id, quantity))
        pass

    def edit_product_info(self, user_id: str, store_id: str, product_id: str, new_product_info):
        # TODO: I've changed the ProductInfo into ProductPurchaseRequest, Asaf.
        # todo: also, wtf is the point of editing this unused object? i think it should be editing product obj not info
        """
        II.4.1.3

        :param user_id:
        :param store_id:
        :param product_id:
        :param new_product_info:
        :return:

        """
        return Response(self.store_controller.edit_product_info(user_id, store_id, product_id,
                                                                self.__service_product_info_to_domain(new_product_info)))

    def __service_product_info_to_domain(self, product_info):
        """
        converts service product info into domain product info
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
        TODO: follow specification
        II.4.4
        :param user_id:
        :param store_id:
        :param new_owner_id:
        :return:
        """
        if not self.user_controller.is_logged_in(user_id):
            return Response(msg="Not logged in")
        if not self.user_controller.is_member(new_owner_id):
            return Response(msg="New owner is not a member")
        return Response(self.store_controller.add_store_owner(user_id, store_id, new_owner_id))

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
        assign the new desired manager as a store manager with default permissions.
        :param user_id:
        :param store_id:
        :param new_manager_id: should be the new manager's username
        :return:
        """
        if not self.user_controller.is_logged_in(user_id):
            return Response(msg="Not logged in")
        if not self.user_controller.is_member(new_manager_id):
            return Response(msg="New owner is not a member")
        return Response(self.store_controller.add_store_manager(user_id, store_id, new_manager_id))
        pass

    def change_manager_permission(self, user_id: str, store_id: str, manager_id: str, new_permission: Permission):
        """
        replaces the permissions of the manager with manager_id with the new permissions.
        II.4.7
        :param user_id:
        :param store_id:
        :param manager_id:
        :param new_permission:
        :return:
        """
        if not self.user_controller.is_logged_in(user_id):
            return Response(msg="Not logged in")
        return Response(self.store_controller.change_manager_permission(
            user_id, store_id, manager_id, self.__service_permissions_to_domain(new_permission)))

    def __service_permissions_to_domain(self, permissions):
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
        close the store - makes it inactive
        II.4.9
        :param user_id:
        :param store_id:
        :return:
        """
        if not self.user_controller.is_logged_in(user_id):
            return Response(msg="Not logged in")
        return Response(self.store_controller.close_store(user_id, store_id))
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
        returns list of manager and owners with their permissions
        II.4.11
        :param user_id:
        :param store_id:
        :return:
        """
        if not self.user_controller.is_logged_in(user_id):
            return Response(msg="Not logged in")
        return Response(self.store_controller.get_store_roles(user_id, store_id))
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
        returns the store's purchase history
        II.4.13
        :param user_id:
        :param store_id:
        :return:
        """
        if not self.user_controller.is_logged_in(user_id):
            return Response(msg="Not logged in")
        return Response(self.store_controller.get_store_purchase_history(user_id, store_id))
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
        if not self.user_controller.is_logged_in(user_id):
            return Response(msg="Not logged in")
        return Response(self.market.get_stores_purchase_history_by_admin(user_id, store_id))
        pass

    def get_system_statistic_by_admin(self, user_id: str):
        """
        II.6.5
        :param user_id:
        :return:
        """
        pass
