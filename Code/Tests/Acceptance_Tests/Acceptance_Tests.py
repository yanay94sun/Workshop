import unittest

from Code.Backend.Domain.DomainDataObjects.ProductPurchaseRequest import ProductPurchaseRequest
from Code.Backend.Service.Service import Service
from Code.Tests.Acceptance_Tests.Initialized_objects import *
manager_id = None
service = Service()
service.initial_system()


def is_error(response):
    return response.msg is not None


class AcceptanceTests(unittest.TestCase):
    def setUp(self):
        self.guest_id = service.enter_as_guest().value
        self.store_id = None

    def test_contact_payment_service(self):
        """
        I.3

        """
        response = service.contact_payment_service(good_payment_info)
        self.assertTrue(not is_error(response), "Should not be an error")
        response = service.contact_payment_service(bad_amount_payment_info)
        self.assertTrue(is_error(response), "Should be an error")
        response = service.contact_payment_service(bad_expiration_payment_info)
        self.assertTrue(is_error(response), "Should be an error")

    def test_contact_supply_service(self):
        """
        I.4
        TODO
        """
        pass

    """
    Users requirements
    General guest actions
    """

    def test_enter_as_guest(self):
        """
        II.1.1

        """
        response = service.enter_as_guest()
        self.assertTrue(not is_error(response), "Should not be an error")

    def test_register(self):
        """
        II.1.3

        """
        response = service.register(self.guest_id, good_register_info)
        self.assertTrue(not is_error(response), "Should not be an error")
        response = service.register(self.guest_id, good_register_info)
        self.assertTrue(is_error(response), "Can not register with a registered id")

    def test_login(self):
        """
        II.1.4

        """
        username = good_register_info["username"]
        password = good_register_info["password"]
        wrong_password = password + 'a'
        # wrong password check
        response = service.login(self.guest_id, username, wrong_password)
        self.assertTrue(is_error(response))
        # good login
        response = service.login(self.guest_id, username, password)
        self.assertTrue(not is_error(response))
        # already logged in
        response = service.login(self.guest_id, username, password)
        self.assertTrue(is_error(response), "Already logged in")

    def test_open_store(self):
        """
        II.3.2

        """
        # check first there are no open stores yet
        response = service.get_stores_info(self.guest_id)
        self.assertTrue(is_error(response))  # error if no stores, TODO maybe change this logic?

        response = service.open_store(self.guest_id, store_name)
        self.assertTrue(not is_error(response))
        self.assertTrue(response.value is not None, "Should return store's id")
        self.store_id = response.value
        response = service.open_store(self.guest_id, "my_store")
        self.assertTrue(is_error(response), "store already exists")

    def test_add_products_to_inventory(self):
        """
        II.4.1.1

        """
        # assert the store is empty first
        self.__check_products_of_store(expected_products=[])
        # add a product
        response = service.add_products_to_inventory(self.guest_id, self.store_id, product1_id, 1)
        self.assertTrue(not is_error(response))
        self.__check_products_of_store(expected_products=["default name"])

    def __check_products_of_store(self, expected_products):
        response = service.get_store_info(self.guest_id, self.store_id)
        self.assertTrue(not is_error(response))
        self.assertTrue(response.value is not None)
        store_info = response.value
        self.assertTrue(store_info["founder_id"] == self.guest_id)
        self.assertTrue(store_info["store_name"] == store_name)
        self.assertTrue(store_info["ID"] == self.store_id)
        self.assertTrue(store_info["products"] == expected_products)

    def test_edit_product_info(self):
        """
        II.4.1.3
        TODO
        """
        # response = service.edit_product_info(self.guest_id, self.store_id, product1_id, )

        pass

    def test_remove_products_from_inventory(self):
        """
        II.4.1.2

        """
        # add a new product
        response = service.add_products_to_inventory(self.guest_id, self.store_id, product2_id, 1)
        self.assertTrue(not is_error(response))
        self.__check_products_of_store(expected_products=["default name"] * 2)
        # remove the product
        response = service.remove_products_from_inventory(self.guest_id, self.store_id, product2_id, 1)
        self.assertTrue(not is_error(response))
        self.__check_products_of_store(expected_products=["default name"])
        # same with more than 1 in quantity
        response = service.add_products_to_inventory(self.guest_id, self.store_id, product2_id, 2)
        self.assertTrue(not is_error(response))
        self.__check_products_of_store(expected_products=["default name"] * 2)
        response = service.remove_products_from_inventory(self.guest_id, self.store_id, product2_id, 1)
        self.assertTrue(not is_error(response))
        self.__check_products_of_store(expected_products=["default name"] * 2)

    """Guest's Purchase actions"""

    def test_get_store_info(self):
        """
        II.2.1
        Tested in 'test_add_products_to_inventory'
        """
        pass

    def test_search_product(self):
        """
        II.2.2
        TODO
        """
        pass

    def test_add_product_to_shop_cart(self):
        """
        II.2.3

        """
        response = service.add_product_to_shoppping_cart(self.guest_id, self.store_id, product1_id, 1)
        self.assertTrue(not is_error(response))
        response = service.get_shopping_cart(self.guest_id)
        self.assertTrue(not is_error(response))
        self.assertIsNotNone(response.value)
        cart = response.value
        basket = cart[self.store_id]
        self.assertTrue(basket[product1_id] == 1)
        # bad add
        response = service.add_product_to_shoppping_cart(self.guest_id, self.store_id, product1_id, 2)
        self.assertTrue(is_error(response))

    def test_get_shop_cart(self):
        """
        II.2.4
        Tested in 'test_add_product_to_shop_cart'
        """

    def test_remove_product_from_shop_cart(self):
        """
        II.2.4

        """
        # bad remove
        response = service.remove_product_from_shopping_cart(self.guest_id,
                                                             ProductPurchaseRequest(self.store_id, product1_id, 2))
        self.assertTrue(is_error(response))
        # good remove
        response = service.remove_product_from_shopping_cart(self.guest_id,
                                                             ProductPurchaseRequest(self.store_id, product1_id, 1))
        self.assertTrue(not is_error(response))

    def test_purchase_shop_cart(self):
        """
        II.2.5
        TODO: test product race condition, (test bad payment as well?)
        """
        service.add_product_to_shoppping_cart(self.guest_id, self.store_id, product1_id, 1)
        response = service.purchase_shopping_cart(self.guest_id, good_payment_info)
        self.assertTrue(not is_error(response))
        self.__check_products_of_store(expected_products=[])
        response = service.get_shopping_cart(self.guest_id)
        self.assertTrue(not is_error(response))
        self.assertIsNotNone(response.value)
        cart = response.value
        with self.assertRaises(KeyError):
            cart[self.store_id]

    """Member's purchase actions"""

    def test_logout(self):
        """
        II.3.1

        """
        # prepare shopping cart
        response = service.add_products_to_inventory(self.guest_id, self.store_id, product1_id, 1)
        self.assertTrue(not is_error(response))
        response = service.add_product_to_shoppping_cart(self.guest_id, self.store_id, product1_id, 1)
        self.assertTrue(not is_error(response))
        # TODO finish
        pass

    def test_exit(self):
        """
        II.1.2

        """

        pass

    # def test_review_product(self):
    #     """
    #     II.3.3
    #
    #     """
    #     pass
    #
    # def test_grade_product(self):
    #     """
    #     II.3.4.1
    #
    #     """
    #     pass
    #
    # def test_grade_store(self):
    #     """
    #     II.3.4.2
    #
    #     """
    #     pass
    #
    # def test_contact_store(self):
    #     """
    #     II.3.5
    #
    #     """
    #     pass
    #
    # def test_complaint(self):
    #     """
    #     II.3.6
    #
    #     """
    #     pass
    #
    # def test_get_personal_purchase_history(self):
    #     """
    #     II.3.7
    #
    #     """
    #     pass
    #
    # def test_get_personal_info(self):
    #     """
    #     II.3.8
    #
    #     """
    #     pass
    #
    # def test_edit_personal_info(self):
    #     """
    #     II.3.8
    #
    #     """
    #     pass
    #
    # def test_upgrade_member_security(self):
    #     """
    #     II.3.9
    #
    #     """
    #     pass

    # def test_edit_store_policy(self):
    #     """
    #     II.4.2
    #     *NOT*  need to implement to this version
    #
    #     """
    #     pass
    #
    # def test_change_purchase_policy(self):
    #     """
    #     II.4.3.1
    #
    #     """
    #     pass
    #
    # def test_change_discount_policy(self):
    #     """
    #     II.4.3.2
    #
    #     """
    #     pass

    def test_add_store_owner(self):
        """
        II.4.4

        """
        # prepare new member
        new_owner_id = self.register_new_guest()
        # check precondition
        response = service.get_store_roles(self.guest_id, self.store_id)
        self.assertTrue(not is_error(response), "Should not be an error")
        self.assertIsNotNone(response.value)
        officials = response.value
        self.assertTrue(len(officials) == 1 and officials[self.guest_id])  # fooya!
        # test
        response = service.add_store_owner(self.guest_id, self.store_id, new_owner_id)
        self.assertTrue(not is_error(response), "Should not be an error")
        response = service.get_store_roles(self.guest_id, self.store_id)
        self.assertTrue(not is_error(response), "Should not be an error")
        self.assertIsNotNone(response.value)
        officials = response.value
        self.assertTrue(len(officials) == 2 and officials[self.guest_id] and officials[new_owner_id])  # bad! really bad
        pass

    def register_new_guest(self):
        response = service.enter_as_guest()
        self.assertTrue(not is_error(response), "Should not be an error")
        self.assertIsNotNone(response.value)
        new_owner_id = response.value
        response = service.register(new_owner_id, {"username": "new_owner", "password": "123"})
        self.assertTrue(not is_error(response), "Should not be an error")
        return new_owner_id

    # def test_remove_store_owner(self):
        #     """
        #     II.4.5
        #
        #     """
        #     pass

    def test_add_store_manager(self):
        """
        II.4.6

        """
        global manager_id
        manager_id = self.register_new_guest()
        response = service.add_store_manager(self.guest_id, self.store_id, manager_id)
        self.assertTrue(not is_error(response), "Should not be an error")
        response = service.get_store_roles(self.guest_id, self.store_id)
        self.assertTrue(not is_error(response), "Should not be an error")
        self.assertIsNotNone(response.value)
        officials = response.value
        self.assertTrue(len(officials) == 3 and officials[self.guest_id] and officials[manager_id])  # Shema Israel

    def test_change_manager_permission(self):
        """
        II.4.7
        TODO
        """
        pass

    # def test_remove_store_manager(self):
    #     """
    #     II.4.8
    #
    #     """
    #     pass

    def test_close_store(self):
        """
        II.4.9

        """
        pass

    # def test_reopen_store(self):
    #     """
    #     II.4.10
    #
    #     """
    #     pass

    def test_get_store_roles(self):
        """
        II.4.11
        Tested in 'test_add_store_owner'
        """
        pass

    # def test_get_users_messages(self):
    #     """
    #     II.4.12.1
    #
    #     """
    #     pass
    #
    # def test_reply_users_messages(self):
    #     """
    #     II.4.12.2
    #
    #     """
    #     pass

    def test_get_store_purchase_history(self):
        """
        II.4.13

        """
        response = service.get_store_purchase_history(self.guest_id, self.store_id)
        self.assertTrue(not is_error(response))
        self.assertIsNotNone(response.value)
        purchase_history = response.value
        self.assertTrue(len(purchase_history) == 1)
        purchase = purchase_history[0]
        self.assertTrue(purchase.product_name == product1_name and purchase.quantity == 1)

    # def test_close_store_permanently(self):
    #     """
    #     II.6.1
    #
    #     """
    #     pass
    #
    # def test_remove_member(self):
    #     """
    #     II.6.2
    #
    #     """
    #     pass
    #
    # def test_get_all_users_messages_by_admin(self):
    #     """
    #     II.6.3.1
    #
    #     """
    #     pass
    #
    # def test_reply_users_messages_by_admin(self):
    #     """
    #     II.6.3.2
    #
    #     """
    #     pass

    def test_get_stores_purchase_history_by_admin(self):
        """
        II.6.4
        TODO
        """
        pass

    # def test_get_system_statistic_by_admin(self):
    #     """
    #     II.6.5
    #
    #     """
    #     pass


if __name__ == '__main__':
    unittest.main()
