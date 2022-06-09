import threading
from typing import Dict

from Code.Backend.Domain.Controllers.Market import Market
from Code.Backend.Domain.Controllers.StoreController import StoreController
from Code.Backend.Domain.Controllers.UserController import UserController
from Code.Backend.Domain.DomainDataObjects.ProductPurchaseRequest import ProductPurchaseRequest
from Code.Backend.Domain.DomainPackageInfo import DomainPackageInfo
from Code.Backend.Domain.DomainPaymentInfo import DomainPaymentInfo
from Code.Backend.Domain.MFResponse import Response
from Code.Backend.Domain.StoreOfficials.Permissions import Permissions
from Code.Backend.Service.Objects.ContactInfo import ContactInfo
from Code.Backend.Service.Objects.PackageInfo import PackageInfo
from Code.Backend.Service.Objects.PaymentInfo import PaymentInfo
from Code.Backend.Service.Objects.PersonalInfo import PersonalInfo


# from Code.Backend.Service.Objects.ProductSearchFilters import Product_search_filters


class Facade:
    def __init__(self):
        self.user_controller: UserController = None
        self.market: Market = None
        self.store_controller: StoreController = None
        self.purchase_lock = threading.Condition()

    """Functional requirements"""

    def initial_system(self, admin_id: str, admin_pwd: str,
                       payment_service, supply_service):
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
        marketResponse = Market().init(admin_id, admin_pwd, payment_service, supply_service)
        if not marketResponse.error_occurred():
            self.market = marketResponse.value
            self.user_controller = UserController()
            self.store_controller = StoreController()
        return marketResponse

    def contact_payment_service(self, payment_info: DomainPaymentInfo) -> Response:
        """
        I.3
        a payment transaction with the current payment service, with the given payment information.
        :param payment_info: the data the payment service needs to successfully manage the payment.
        :return: Response object
        """
        return self.market.contact_payment_service(payment_info)

    def change_payment_service(self, payment_service):
        return self.market.connect_payment_service(payment_service)

    def change_supply_service(self, supply_service):
        return self.market.connect_supply_service(supply_service)

    def contact_supply_service(self, package_info: DomainPackageInfo) -> Response:
        """
        I.4
        a request for a delivery from the supply service.
        :param package_info: the data the current supply service needs to successfully process the request.
        :return:
        """
        return self.market.contact_supply_service(package_info)

    """
    Users requirements
    General guest actions
    """

    def enter_as_guest(self) -> Response:
        """
        II.1.1
        generates a temp id and creates a Visitor object with a default guest state and a shopping cart.
        :return: guest id
        """
        return self.user_controller.create_guest()

    def exit(self, user_id: str):
        """
        II.1.2
        when a guest is exit, all its data is dismissed including its shopping cart.
        :param user_id:
        :return:
        """
        return self.user_controller.exit(user_id)

    def register(self, guest_id: str, user_info: Dict):
        """
        II.1.3
        register a user to the market, creates a member state.
        :param guest_id:
        :param user_info: all info needed for registration.
        :return:
        """
        return self.user_controller.register(guest_id, user_info)

    def login(self, guest_id: str, username: str, password: str):
        """
        II.1.4
        changes state to logged in
        :param guest_id:
        :param username:
        :param password:
        :return:
        """
        return self.user_controller.login(guest_id, username, password)

    """Guest's Purchase actions"""

    def get_store_info(self, store_id: str) -> Response:
        """
        II.2.1.1
        when a user request for a specific store info.
        param store_id:
        :return: Store's info which contains:
        store's name, store's owners, rank, products
        """
        return self.store_controller.get_store_info(store_id)

    def get_stores_info(self) -> Response:
        """
        II.2.1.2
        when a user request for all stores info.
        return: List of store info
        """
        return self.store_controller.get_stores_info()
        pass

    def search_product(self, search_text: str, by_name, by_category, filter_type,
                       filter_value):
        """
        II.2.2
        Search a product by given product name, category or key words.
        Filtering results by given feature filters
        :param search_text:
        :param by_name:
        :param by_category:
        :param: filter_type:
        :param filter_value:
        :return:
        """
        return self.store_controller.search_product(search_text, by_name, by_category, filter_type, filter_value)

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
        cart = self.user_controller.get_shopping_cart(user_id)
        if cart.error_occurred():
            return cart
        cart = cart.value
        # print(cart)
        # print(cart.shopping_baskets)
        if store_id not in cart.shopping_baskets:
            total_quantity = 0
        else:
            basket = cart.shopping_baskets[store_id]
            # print(basket)
            list_of_prod = basket.get_products_and_quantities()
            # print(list_of_prod)
            if product_id not in list_of_prod:
                total_quantity = 0
            else:
                total_quantity = list_of_prod[product_id]
        # print(total_quantity)
        # total_quantity = self.user_controller.get_shopping_cart(user_id). \
        #     value.shopping_baskets[store_id].get_products_and_quantities()[product_id]
        prod_pur_req_response = self.store_controller.create_product_purchase_request(store_id, product_id,
                                                                                      total_quantity + quantity)
        # check if error occurred
        if not prod_pur_req_response.error_occurred():
            prod_pur_req_response.value.quantity -= total_quantity
            return self.user_controller.add_product_to_shop_cart(user_id, prod_pur_req_response.value)
        return prod_pur_req_response

    def get_shopping_cart(self, user_id: str) -> Response:
        """
        II.2.4
        return the information of the user shopping cart.
        param user_id:
        :return: Shopping cart object
        """
        return self.user_controller.get_shopping_cart(user_id)

    def remove_product_from_shopping_cart(self, user_id: str, ppr: ProductPurchaseRequest):
        """
        II.2.4

        :param user_id:
        :param ppr:
        :return:
        """
        return self.user_controller.remove_product_from_shopping_cart(user_id, ppr)

    def get_cart_price(self, user_id):
        with self.purchase_lock:
            """
            valid products quantities
            get price for baskets (apply disc)
            reduce products from store
            pay
            revert if could not pay
            """
            cart = self.user_controller.get_shopping_cart(user_id)
            all_products = [p for p in cart.value.iter_products()]
            all_baskets = cart.value.shopping_baskets
            # validate cart
            if not self.store_controller.valid_all_products_for_purchase(all_products):
                return Response(msg="not enough quantities")
            # get prices
            prices = (self.store_controller.get_basket_price(store_id, basket) for store_id, basket in all_baskets.items())
            total_price = 0
            for p in prices:
                if p.error_occurred():
                    return Response.from_error("some error occurred while calculating a basket's price")
                total_price += p.value
            # if any((price.error_occurred() for price in prices)):
            #     return Response.from_error("some error occurred while calculating a basket's price")
            # total_price = sum((price.value for price in prices))
            return Response(total_price)

    def purchase_shopping_cart(self, user_id: str, payment_info: DomainPaymentInfo):
        # TODO still
        """
        II.2.5
        gets user's shopping cart and applies discount policies on each basket, then decrease the quantity of the
        product in the store
        supports only instant purchase
        :param user_id:
        :param payment_info
        :return:
        """
        with self.purchase_lock:
            """
            valid products quantities
            get price for baskets (apply disc)
            reduce products from store
            pay
            revert if could not pay
            """
            cart = self.user_controller.get_shopping_cart(user_id)
            all_products = [p for p in cart.value.iter_products()]
            all_baskets = cart.value.shopping_baskets
            # validate cart
            if not self.store_controller.valid_all_products_for_purchase(all_products):
                return Response(msg="not enough quantities")
            # get prices
            prices = (self.store_controller.get_basket_price(store_id, basket) for store_id, basket in
                      all_baskets.items())
            # if any((price.error_occurred() for price in prices)):
            #     return Response.from_error("some error occurred while calculating a basket's price")
            # total_price = sum((price.value for price in prices))
            total_price = 0
            for p in prices:
                if p.error_occurred():
                    return Response.from_error("some error occurred while calculating a basket's price")
                total_price += p.value
            if total_price != payment_info.amount_to_pay:
                return Response(msg="You little piece of shit, trying to steal aha?")
            # good pay, remove products from shopping cart
            response = self.market.contact_payment_service(payment_info)
            if response.error_occurred():
                return response
            success = response.value
            if success:
                for p in all_products:
                    response = self.remove_product_from_shopping_cart(user_id, p)
                    if response.error_occurred():
                        return response
                # remove products from inventories
                response = self.store_controller.remove_all_products_for_purchasing(all_products)
                if response.error_occurred():
                    return response
            else:
                return Response.from_error("unsuccessfully payment")


        # pay, if error occured revert
        # revert: self.store_controller.revert_purchase_requests(all_products)
        #  purchase_history = Purchase()
        #  self.user_controller.update_purchase_history(purchase_history)
        # self.store_controller.update_purchase_history(purchase_history)

    """
    --------------------------------------
    Member's purchase actions
    --------------------------------------
    """

    def logout(self, user_id: str):
        """
        II.3.1
        Logging out, the shopping cart is saved.
        :param user_id:
        :return:
        """
        if not self.user_controller.is_logged_in(user_id):
            return Response(msg="Not logged in")
        return self.user_controller.logout(user_id)

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
        response_member_id = self.user_controller.get_users_username(user_id)
        if response_member_id.error_occurred():
            return response_member_id
        return self.store_controller.open_store(response_member_id.value, store_name)

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

    def get_personal_purchase_history(self, user_id: str):
        """
        Nitzan: put the responsibility in the user
        II.3.7

        :param user_id:
        :return:
        """
        pass

    def get_personal_info(self, user_id: str):
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
        adds the given product's quantity to the store's inventory.,
        :param user_id:
        :param store_id:
        :param product_id:
        :param quantity:
        :return:
        """
        if not self.user_controller.is_logged_in(user_id):
            return Response(msg="Not logged in")
        member_id = self.user_controller.get_users_username(user_id)
        if member_id.error_occurred():
            return member_id
        return self.store_controller.add_products_to_inventory(member_id.value, store_id, product_id, quantity)

    # new function in version 2
    def add_new_product_to_inventory(self, user_id: str, store_id: str,
                                     product_name: str, product_description
                                     , price: int, category: str):
        if not self.user_controller.is_logged_in(user_id):
            return Response(msg="Not logged in")
        member_id = self.user_controller.get_users_username(user_id)
        if member_id.error_occurred():
            return member_id
        return self.store_controller.add_new_product_to_inventory(member_id.value,
                                                                  store_id,
                                                                  product_name,
                                                                  product_description,
                                                                  price, category)

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
        member_id = self.user_controller.get_users_username(user_id)
        if member_id.error_occurred():
            return member_id
        return self.store_controller.remove_products_from_inventory(member_id.value, store_id, product_id, quantity)

    def edit_product_info(self, user_id: str, store_id: str, product_id: str, name, description, rating
                          , price, category):
        """
        II.4.1.3

        :param user_id:
        :param store_id:
        :param product_id:
        :param name:
        :param description:
        :param price:
        :param rating:
        :param category:
        :return:

        """
        if not self.user_controller.is_logged_in(user_id):
            return Response(msg="Not logged in")
        member_id = self.user_controller.get_users_username(user_id)
        if member_id.error_occurred():
            return member_id
        return self.store_controller.edit_product_info(member_id.value, store_id, product_id, name, description, rating,
                                                       price, category)

    def edit_store_policy(self, user_id: str, store_id: str):
        """
        II.4.2
        *NOT*  need to implement to this version
        :param user_id:
        :param store_id:
        :return:
        """
        pass

    def change_purchase_policy(self, user_id: str, store_id: str, purchase_policy):
        """
        II.4.3.1
        :param user_id:
        :param store_id:
        :param purchase_policy:
        :return:
        """
        pass

    def change_discount_policy(self, user_id: str, store_id: str, discount_policy):
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
        :param new_owner_id: the new owner's *member_id*
        :return:
        """
        if not self.user_controller.is_logged_in(user_id):
            return Response(msg="Not logged in")
        if not self.user_controller.is_member(new_owner_id):
            return Response(msg="New owner is not a member")
        member_id = self.user_controller.get_users_username(user_id)
        if member_id.error_occurred():
            return member_id
        return self.store_controller.add_store_owner(member_id.value, store_id, new_owner_id)

    def remove_store_owner(self, user_id: str, store_id: str, subject_username: str):
        """
        II.4.5
        :param user_id:
        :param store_id:
        :param subject_username:
        :return:
        """
        if not self.user_controller.is_logged_in(user_id):
            return Response.from_error("user is not logged in")
        remover_username = self.user_controller.get_users_username(user_id)
        if remover_username.error_occurred():
            return remover_username
        return self.store_controller.remove_store_owner(remover_username.value, store_id, subject_username)

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
        member_id = self.user_controller.get_users_username(user_id)
        if member_id.error_occurred():
            return member_id
        return self.store_controller.add_store_manager(member_id.value, store_id, new_manager_id)

    def change_manager_permission(self, user_id: str, store_id: str, manager_id: str, new_permission):
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
        member_id = self.user_controller.get_users_username(user_id)
        if member_id.error_occurred():
            return member_id
        return self.store_controller.change_manager_permission(
            member_id.value, store_id, manager_id, new_permission)

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
        return self.store_controller.close_store(user_id, store_id)
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
        member_id = self.user_controller.get_users_username(user_id)
        if member_id.error_occurred():
            return member_id
        return self.store_controller.get_store_roles(member_id.value, store_id)
        pass

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
        if not self.user_controller.is_logged_in(user_id):
            return Response(msg="Not logged in")
        member_id = self.user_controller.get_users_username(user_id)
        if member_id.error_occurred():
            return member_id
        return self.store_controller.get_store_purchase_history(member_id.value, store_id)
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

    def get_stores_purchase_history_by_admin(self, user_id: str, store_id):
        """
        II.6.4
        :param user_id:
        :param store_id:
        :return:
        """
        if not self.user_controller.is_logged_in(user_id):
            return Response(msg="Not logged in")
        if not self.market.check_if_admin(user_id):
            return Response(msg="Not admin")
        member_id = self.user_controller.get_users_username(user_id)
        if member_id.error_occurred():
            return member_id
        return self.store_controller.get_store_purchase_history(member_id.value, store_id, is_admin=True)

    def get_system_statistic_by_admin(self, user_id: str):
        """
        II.6.5
        :param user_id:
        :return:
        """
        pass

    def get_users_stores(self, user_id: str):
        if not self.user_controller.is_logged_in(user_id):
            return Response(msg="Not logged in")
        member_id = self.user_controller.get_users_username(user_id)
        if member_id.error_occurred():
            return member_id
        res = self.store_controller.get_officials_stores(member_id.value)
        return Response(value=res)

    def is_logged_in(self, user_id: str):
        if self.user_controller.is_logged_in(user_id):
            return Response(value=True)
        else:
            return Response(value=False)

    def get_product_and_quantities(self, store_id, product_id):
        return self.store_controller.get_product_and_quantities(store_id, product_id)

    def get_permissions(self, store_id, user_id):
        if not self.user_controller.is_logged_in(user_id):
            return Response(msg="Not logged in")
        member_id = self.user_controller.get_users_username(user_id)
        if member_id.error_occurred():
            return member_id
        if not self.user_controller.is_member(member_id.value):
            permissions = {}
            for i in range(0, 7):
                permissions[i] = False
            return Response(value=permissions)
        member_id = self.user_controller.get_users_username(user_id)
        if member_id.error_occurred():
            return member_id
        return self.store_controller.get_permissions(store_id, member_id.value)



# if __name__ == '__main__':
#     fc = Facade()
#     print(fc.enter_as_guest().msg)
#     print(fc.register("1", {"username": "Tomer", "password": "123"}).value)
#     print(fc.open_store("1", "theStore").msg)
#     print(fc.get_permissions("1","1").value)
#     print(fc.enter_as_guest().msg)
#     print(fc.register("2", {"username": "Tal", "password": "123"}).msg)
#     # print(fc.open_store("2", "theStore2").msg)
#     # print(fc.add_new_product_to_inventory("1", "1", "apple", "", 2, "").msg)
#     print(fc.add_store_owner("1", "1", "Tal").msg)
#     print(fc.get_permissions("1","2").value)

    # print(fc.add_new_product_to_inventory("2", "1", "apple", "", 2, "").msg)
    # print(fc.change_manager_permission("1", "1", "Tal", {1: True, 2: False,
    #                                                      3: False, 4: False, 5: False, 6: False, 7: False}).msg)
    # print(fc.add_new_product_to_inventory("2", "1", "apple juice", "", 2, "").msg)
