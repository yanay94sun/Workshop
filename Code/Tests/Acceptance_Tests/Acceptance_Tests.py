import unittest
from Code.Backend.Service.Service import Service
service = Service()
service.initial_system()


class AcceptanceTests(unittest.TestCase):

    def initial_system(self):
        """
        I.1

        """
        pass

    def contact_payment_service(self):
        """
        I.3

        """
        pass

    def contact_supply_service(self):
        """
        I.4

        """
        pass

    """
    Users requirements
    General guest actions
    """

    def enter_as_guest(self):
        """
        II.1.1

        """

    def exit(self):
        """
        II.1.2

        """
        pass

    def register(self):
        """
        II.1.3

        """
        pass

    def login(self):
        """
        II.1.4

        """
        pass

    """Guest's Purchase actions"""

    def get_store_info(self):
        """
        II.2.1

        """
        pass

    def search_product(self):
        """
        II.2.2

        """

        pass

    def add_product_to_shop_cart(self):
        """
        II.2.3

        """
        pass

    def get_shop_cart(self):
        """
        II.2.4

        """

    def remove_product_from_shop_cart(self):
        """
        II.2.4

        """

    def purchase_shop_cart(self):
        """
        II.2.5

        """
        pass

    """Member's purchase actions"""

    def logout(self):
        """
        II.3.1

        """
        pass

    def open_store(self):
        """
        II.3.2

        """
        pass

    def review_product(self):
        """
        II.3.3

        """
        pass

    def grade_product(self):
        """
        II.3.4.1

        """
        pass

    def grade_store(self):
        """
        II.3.4.2

        """
        pass

    def contact_store(self):
        """
        II.3.5

        """
        pass

    def complaint(self):
        """
        II.3.6

        """
        pass

    def get_personal_purchase_history(self):
        """
        II.3.7

        """
        pass

    def get_personal_info(self):
        """
        II.3.8

        """
        pass

    def edit_personal_info(self):
        """
        II.3.8

        """
        pass

    def upgrade_member_security(self):
        """
        II.3.9

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
    def manage_inventory(self):
        """
        II.4.1
        TODO: maybe to split this into 3 funcs???
        add, remove and edit the inventory

        """
        pass

    def edit_store_policy(self):
        """
        II.4.2
        *NOT*  need to implement to this version

        """
        pass

    def change_purchase_policy(self):
        """
        II.4.3.1

        """
        pass

    def change_discount_policy(self):
        """
        II.4.3.2

        """
        pass

    def add_store_owner(self):
        """
        II.4.4

        """
        pass

    def remove_store_owner(self):
        """
        II.4.5

        """
        pass

    def add_store_manager(self):
        """
        II.4.6

        """
        pass

    def change_manager_permission(self):
        """
        II.4.7

        """
        pass

    def remove_store_manager(self):
        """
        II.4.8

        """
        pass

    def close_store(self):
        """
        II.4.9

        """
        pass

    def reopen_store(self):
        """
        II.4.10

        """
        pass

    def get_store_roles(self):
        """
        II.4.11

        """
        pass

    def get_users_messages(self):
        """
        II.4.12.1

        """
        pass

    def reply_users_messages(self):
        """
        II.4.12.2

        """
        pass

    def get_store_purchase_history(self):
        """
        II.4.13

        """
        pass

    def close_store_permanently(self):
        """
        II.6.1

        """
        pass

    def remove_member(self):
        """
        II.6.2

        """
        pass

    def get_all_users_messages_by_admin(self):
        """
        II.6.3.1

        """
        pass

    def reply_users_messages_by_admin(self):
        """
        II.6.3.2

        """
        pass

    def get_stores_purchase_history_by_admin(self):
        """
        II.6.4

        """
        pass

    def get_system_statistic_by_admin(self):
        """
        II.6.5

        """
        pass


if __name__ == '__main__':
    unittest.main()
