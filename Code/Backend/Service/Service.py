from Service import Shopcart_info
from Service.Contact_info import Contact_info
from Service.Package_info import Package_info
from Service.Payment_info import Payment_info
from Service.Personal_info import Personal_info
from Service.Personal_purchase_history import Personal_purchase_history
from Service.Product_search_filters import Product_search_filters
from Service.Product_info import Product_info
from Service.Response import Response
from Service.Store_info import Store_info


class Service:
    def __init__(self):
        pass

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

    def enter_as_guest(self, guest_id: str):
        """
        II.1.1
        :return:
        """
        pass

    def guest_exit(self, guest_id: str):
        """
        II.1.2.1
        :param guest_id:
        :return:
        """
        pass

    def member_exit(self, user_id: str):
        """
        II.1.2.2
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

    def get_product_info(self, user_id: str, product_id) -> Product_info:
        """
        II.2.1

        :param user_id:
        :param product_id:
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

    def review_product(self, user_id: str, review: str):
        """
        II.3.3
        :param user_id:
        :param review:
        :return:
        """
        pass

    def grade_product(self, user_id: str, product_id: str, grade):
        """
        II.3.4
        :param user_id:
        :param product_id:
        :param grade:
        :return:
        """
        pass

    def grade_store(self, user_id: str, store_id: str, grade):
        """
        II.3.4
        :param user_id:
        :param store_id:
        :param grade:
        :return:
        """
        pass

    def contact_store(self, user_id: str, store_id: str, contact_info: Contact_info):
        """
        II.3.5

        :param user_id:
        :param store_id:
        :param contact_info:
        :return:
        """
        pass

    def complaint(self, user_id: str, comp: Contact_info):
        """
        II.3.6

        :param user_id:
        :param comp:
        :return:
        """
        pass

    def get_personal_purchase_history(self, user_id: str) -> Personal_purchase_history:
        """
        II.3.7

        :param user_id:
        :return:
        """
        pass

    def get_personal_info(self, user_id: str) -> Personal_info:
        """
        II.3.8

        :param user_id:
        :return:
        """
        pass

    def edit_personal_info(self, user_id: str, new_personal_info: Personal_info):
        """
        II.3.8

        :param user_id:
        :param new_personal_info:
        :return:
        """
        pass

    def upgrade_member_security(self, user_id: str):
        """
        II.3.9
        TODO more arguments might be necessary
        :param user_id:
        :return:
        """
        pass

