import unittest
from Code.Backend.Service.Service import Service
from Code.Tests.Acceptance_Tests.Initialized_objects import *
service = Service()
service.initial_system()


class AcceptanceTests(unittest.TestCase):
    def setUp(self):
        pass

    def test_enter_as_guest(self):
        """
        II.1.1

        """

    def test_exit(self):
        """
        II.1.2

        """
        pass

    def test_register(self):
        """
        II.1.3

        """
        pass

    def test_login(self):
        """
        II.1.4

        """
        pass

    """Guest's Purchase actions"""

    def test_get_store_info(self):
        """
        II.2.1

        """
        pass

    def test_search_product(self):
        """
        II.2.2

        """

        pass

    def test_add_product_to_shop_cart(self):
        """
        II.2.3

        """
        pass

    def test_get_shop_cart(self):
        """
        II.2.4

        """

    def test_remove_product_from_shop_cart(self):
        """
        II.2.4

        """

    def test_purchase_shop_cart(self):
        """
        II.2.5

        """
        pass

    """Member's purchase actions"""

    def test_logout(self):
        """
        II.3.1

        """
        pass

    def test_get_personal_info(self):
        """
        II.3.8

        """
        pass

    def test_edit_personal_info(self):
        """
        II.3.8

        """
        pass


if __name__ == '__main__':
    unittest.main()
