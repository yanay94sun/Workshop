import threading
from typing import Dict
from typing import Dict, List
import logging

from Code.Backend.Domain.DomainPackageInfo import DomainPackageInfo
from Code.Backend.Domain.Facade import Facade
from Code.Backend.Service.Objects.PackageInfo import PackageInfo

from Code.Backend.Domain.Controllers.Market import Market
from Code.Backend.Domain.Controllers.StoreController import StoreController
from Code.Backend.Domain.Controllers.UserController import UserController
from Code.Backend.Domain.DomainDataObjects.ProductPurchaseRequest import ProductPurchaseRequest
from Code.Backend.Domain.DM_product_info import DM_product_info
from Code.Backend.Domain.DomainPaymentInfo import DomainPaymentInfo
from Code.Backend.Service.Objects import Shopcart_info
from Code.Backend.Service.Objects.ContactInfo import ContactInfo
from Code.Backend.Service.Objects.DiscountPolicy import DiscountPolicy
from Code.Backend.Service.Objects.PaymentInfo import PaymentInfo
from Code.Backend.Service.Objects.PersonalInfo import PersonalInfo
from Code.Backend.Service.Objects.Personal_purchase_history import Personal_purchase_history
from Code.Backend.Service.Objects.ProductInfo import ProductInfo
from Code.Backend.Service.Objects.ProductSearchFilters import ProductSearchFilters
from Code.Backend.Service.Objects.PurchasePolicy import PurchasePolicy
from Code.Backend.Service.Response import Response
from Code.Backend.Service.Objects.Store_info import Store_info

logging.basicConfig(filename="SystemLog.log")


def write_to_log(response, success_msg):
    if response.error_occurred():
        logging.critical(response.msg)
    else:
        logging.info(success_msg)


class Service:
    def __init__(self):
        self.facade = Facade()

    def initial_system(self, payment_service, supply_service, admin_id: str = None, admin_pwd: str = None):
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
        response = Response(self.facade.initial_system(admin_id, admin_pwd, payment_service, supply_service))
        write_to_log(response, "The system initialized successfully")
        return response

    def contact_payment_service(self, payment_info: PaymentInfo) -> Response:
        """
        I.3
        a payment transaction with the current payment service, with the given payment information.
        :param payment_info: the data the payment service needs to successfully manage the payment.
        :return: Response object
        """
        response = Response(self.facade.contact_payment_service(self.__service_payment_info_to_domain(payment_info)))
        write_to_log(response, "successfully contacted payment service")
        return response

    def change_payment_service(self, payment_service):
        response = Response(self.facade.change_payment_service(payment_service))
        write_to_log(response, "successfully changed payment service")
        return response

    def change_supply_service(self, supply_service):
        response = Response(self.facade.change_supply_service(supply_service))
        write_to_log(response, "successfully changed supply service")
        return response

    def __service_payment_info_to_domain(self, payment_info):
        """ 
        converts ...
        """
        return DomainPaymentInfo(payment_info)

    def contact_supply_service(self, package_info: PackageInfo) -> Response:
        """
        I.4
        a request for a delivery from the supply service.
        :param package_info: the data the current supply service needs to successfully process the request.
        :return:
        """
        response = Response(self.facade.contact_supply_service(self.__service_supply_info_to_domain(package_info)))
        write_to_log(response, "successfully contacted supply service")
        return response

    def __service_supply_info_to_domain(self, package_info):
        """

        """
        return DomainPackageInfo(package_info)

    """
    ---------------------------------------------------
    Users requirements
    General guest actions
    ---------------------------------------------------
    """

    def enter_as_guest(self) -> Response:
        """
        II.1.1
        generates a temp id and creates a Visitor object with a default guest state and a shopping cart.
        :return: guest id
        """
        response = Response(self.facade.enter_as_guest())
        write_to_log(response, "successfully entered as guest")
        return response

    def exit(self, user_id: str):
        """
        II.1.2
        when a guest is exit, all its data is dismissed including its shopping cart.
        :param user_id:
        :return:
        """
        response = Response(self.facade.exit(user_id))
        write_to_log(response, "successfully exited")
        return response

    def register(self, guest_id: str, user_info: Dict):
        """
        II.1.3
        register a user to the market, creates a member state.
        :param guest_id:
        :param user_info: all info needed for registration.
        :return:
        """
        response = Response(self.facade.register(guest_id, user_info))
        write_to_log(response, "successfully register to the system")
        return response

    def login(self, guest_id: str, username: str, password: str):
        """
        II.1.4
        changes state to logged in
        :param guest_id:
        :param username:
        :param password:
        :return:
        """
        response = Response(self.facade.login(guest_id, username, password))
        write_to_log(response, "successfully logged in")
        return response

    """Guest's Purchase actions"""

    def get_store_info(self, store_id: str) -> Response:
        """
        II.2.1.1
        when a user request for a specific store info.
        param store_id:
        return: Store's info which contains:
        store's name, store's owners, rank, products
        """
        response = Response(self.facade.get_store_info(store_id))
        write_to_log(response, "successfully got store info")
        return response

    def get_stores_info(self) -> Response:
        response = Response(self.facade.get_stores_info())
        write_to_log(response, "successfully got stores info")
        return response

    def search_product(self, product_filters: ProductSearchFilters):
        """
        II.2.2
        Search a product by given product name, category or keywords.
        Filtering results by given feature filters
        :param product_filters: An object contains filtering criteria, like price range, product's grade...
        :return:
        """
        response = Response(self.facade.search_product(product_filters.text,
                                                       product_filters.by_name,
                                                       product_filters.by_category,
                                                       product_filters.filter_type,
                                                       product_filters.filter_value))
        write_to_log(response, "successfully searched for products")
        return response

    def add_product_to_shopping_cart(self, user_id: str, store_id, product_id, quantity):
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
        response = Response(self.facade.add_product_to_shopping_cart(user_id, store_id, product_id, quantity))
        write_to_log(response, "successfully added product to shopping cart")
        return response

    def get_shopping_cart(self, user_id: str) -> Response:
        """
        II.2.4
        return the information of the user shopping cart.
        param user_id:
        :return: Shopping cart object
        """
        response = Response(self.facade.get_shopping_cart(user_id))
        write_to_log(response, "successfully got user's shopping cart")
        return response

    def remove_product_from_shopping_cart(self, user_id: str, ppr: ProductPurchaseRequest):
        """
        II.2.4

        :param user_id:
        :param ppr:
        :return:
        """
        response = Response(self.facade.remove_product_from_shopping_cart(user_id, ppr))
        write_to_log(response, "successfully removed product from shopping cart")
        return response

    def purchase_shopping_cart(self, user_id: str, payment_info):
        # TODO not implemented
        """
        II.2.5
        gets user's shopping cart and applies discount policies on each basket, then decrease the quantity of the
        product in the store
        supports only instant purchase
        param user_id:
        payment_info:
        :return:
        """
        response = Response(self.facade.purchase_shopping_cart(user_id, payment_info))
        write_to_log(response, "successfully purchased shopping cart")
        return response

    """
    --------------------------------------
    Member's purchase actions
    --------------------------------------
    """

    def logout(self, user_id: str):
        """
        II.3.1
        Logging out, the shopping cart is saved.
        param user_id:
        :return:
        """
        response = Response(self.facade.logout(user_id))
        write_to_log(response, "successfully logged out")
        return response

    def open_store(self, user_id: str, store_name: str):
        """
        II.3.2
        A registered member may open a store and be the founder and a manager.
        param user_id:
        param store_name: the store's name
        :return:
        """
        response = Response(self.facade.open_store(user_id, store_name))
        write_to_log(response, "successfully opned store")
        return response

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

    def contact_store(self, user_id: str, store_id: str, contact_info: ContactInfo):
        """
        Nitzan: put the responsibility in the store
        II.3.5

        :param user_id:
        :param store_id:
        :param contact_info:
        :return:
        """
        pass

    def complaint(self, user_id: str, comp: ContactInfo):
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

    def get_personal_info(self, user_id: str) -> PersonalInfo:
        """
        Nitzan: put the responsibility in the user
        II.3.8

        :param user_id:
        :return:
        """
        pass

    def edit_personal_info(self, user_id: str, new_personal_info: PersonalInfo):
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
        response = Response(self.facade.add_products_to_inventory(user_id,
                                                                  store_id, product_id, quantity))
        write_to_log(response, "successfully added products to inventory")
        return response

    # new function in version 2
    def add_new_product_to_inventory(self, user_id: str, store_id: str,
                                     product_name: str, product_description
                                     , price: int, category: str):
        response = Response(
            self.facade.add_new_product_to_inventory(user_id, store_id, product_name, product_description, price,
                                                     category))
        write_to_log(response, "successfully added new product")
        return response

    def remove_products_from_inventory(self, user_id: str, store_id: str, product_id: str, quantity: int):
        """
        II.4.1.2

        :param user_id:
        :param store_id:
        :param product_id
        :param quantity:
        :return:
        """
        response = Response(self.facade.remove_products_from_inventory(user_id, store_id, product_id, quantity))
        write_to_log(response, "successfully removed products from inventory")
        return response

    def edit_product_info(self, user_id: str, store_id: str, product_id: str, new_product_info: ProductInfo):
        """
        II.4.1.3

        :param user_id:
        :param store_id:
        :param product_id:
        :param new_product_info:
        :return:

        """
        response = Response(self.facade.edit_product_info(user_id, store_id, product_id, new_product_info.name,
                                                          new_product_info.description, new_product_info.rating,
                                                          new_product_info.price, new_product_info.category))
        write_to_log(response, "successfully edited product info")
        return response

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
        response = Response(self.facade.add_store_owner(user_id, store_id, new_owner_id))
        write_to_log(response, "successfully added store owner")
        return response

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
        response = Response(self.facade.add_store_manager(user_id, store_id, new_manager_id))
        write_to_log(response, "successfully added store manager")
        return response

    def change_manager_permission(self, user_id: str, store_id: str, manager_id: str, new_permission: Dict):
        """
        replaces the permissions of the manager with manager_id with the new permissions.
        II.4.7
        :param user_id:
        :param store_id:
        :param manager_id:
        :param new_permission:
        :return:
        """
        response = Response(self.store_controller.change_manager_permission(
            user_id, store_id, manager_id, new_permission))
        write_to_log(response, "successfully changed manager permissions")
        return response

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
        response = Response(self.facade.close_store(user_id, store_id))
        write_to_log(response, "successfully closed store")
        return response

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
        response = Response(self.facade.get_store_roles(user_id, store_id))
        write_to_log(response, "successfully got store roles")
        return response

    def get_users_messages(self, user_id: str, store_id: str):
        """
        II.4.12.1
        :param user_id:
        :param store_id:
        :return:
        """
        pass

    def reply_users_messages(self, user_id: str, store_id: str, user_contact_info: ContactInfo,
                             owner_contact_info: ContactInfo):
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
        response = Response(self.facade.get_store_purchase_history(user_id, store_id))
        write_to_log(response, "successfully got store purchase history")
        return response

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

    def reply_users_messages_by_admin(self, user_id: str, store_id: str, user_contact_info: ContactInfo,
                                      admin_contact_info: ContactInfo):
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
        response = Response(self.facade.get_stores_purchase_history_by_admin(user_id, store_id))
        write_to_log(response, "successfully got store purchase history by admin")
        return response

    def get_system_statistic_by_admin(self, user_id: str):
        """
        II.6.5
        :param user_id:
        :return:
        """
        pass

    ##################################################################
    # functions for frontend
    ##############################################################
    def get_users_stores(self, user_id: str):
        """
        returns all users stores (id and name)
        """
        response = Response(self.facade.get_users_stores(user_id))
        write_to_log(response, "successfully got stores")
        return response

    def is_logged_in(self, user_id: str):
        response = Response(self.facade.is_logged_in(user_id))
        write_to_log(response, "successfully checked if logged in")
        return response
