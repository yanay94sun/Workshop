import unittest
# login-> fill-> log out  ->log in-> purchase
from Code.Backend.Domain.DomainDataObjects.ProductPurchaseRequest import ProductPurchaseRequest
from Code.Backend.Service.Objects.PaymentService import PaymentService
from Code.Backend.Service.Objects.SupplySevice import SupplyService
from Code.Backend.Service.Service import Service
from Code.Tests.Acceptance_Tests.Initialized_objects import *


def is_error(response):
    return response.msg is not None


class AcceptanceTests(unittest.TestCase):
    def setUp(self):
        self.service = Service()
        self.service.initial_system(admin_id=admin_user, admin_pwd=admin_pass, payment_service=PaymentService(),
                                    supply_service=SupplyService())

    # def test_contact_payment_service(self):
    #     """
    #     I.3
    #
    #     """
    #     response = service.contact_payment_service(good_payment_info)
    #     self.assertTrue(not is_error(response), "Should not be an error")
    #     response = service.contact_payment_service(bad_amount_payment_info)
    #     self.assertTrue(is_error(response), "Should be an error")
    #     response = service.contact_payment_service(bad_expiration_payment_info)
    #     self.assertTrue(is_error(response), "Should be an error")

    def test_1_contact_supply_service(self):
        """
        I.4
        TODO
        """
        pass

    """
    Users requirements
    General guest actions
    """

    def enter_as_guest(self):
        return self.service.enter_as_guest()

    def test_2_enter_as_guest(self):
        """
        II.1.1

        """
        response = self.enter_as_guest()
        self.assertTrue(not is_error(response), "Should not be an error")

    def register(self, user_info):
        response = self.enter_as_guest()
        self.assertTrue(not is_error(response), "Should not be an error when entering as guest")
        self.assertIsNotNone(response.value)
        g_id = response.value
        response = self.service.register(g_id, user_info)
        self.assertTrue(not is_error(response), "Should not be an error when registered once")
        return g_id

    def test_3_register(self):
        """
        II.1.3

        """
        g_id = self.register(good_register_info)
        response = self.service.register(g_id, good_register_info)
        self.assertTrue(is_error(response), "Can not register with a registered id")

    def login(self, register_info):
        g_id = self.register(register_info)
        # response = self.service.login(g_id, register_info["username"], register_info["password"])
        # self.assertTrue(not is_error(response), "Should not be an error when login once with correct info")

    def test_4_login(self):
        """
        II.1.4
        Assumption: after registration the user is logged in
        """
        username = good_register_info["username"]
        password = good_register_info["password"]
        wrong_password = password + 'a'
        g_id = self.register(good_register_info)
        # wrong password check
        response = self.service.login(g_id, username, wrong_password)
        self.assertTrue(is_error(response))
        # good login
        # response = self.service.login(g_id, username, password)
        # self.assertTrue(not is_error(response))

        # already logged in
        response = self.service.login(g_id, username, password)
        self.assertTrue(is_error(response), "Already logged in")

    def test_5_open_store(self):
        """
        II.3.2

        """
        self.login(good_register_info)
        # global store_id
        # check first there are no open stores yet
        response = self.service.get_stores_info()
        self.assertTrue(is_error(response))  # error if no stores
        # open the store
        response = self.service.open_store(good_register_info["username"], store_name)
        self.assertTrue(not is_error(response))
        self.assertIsNotNone(response.value, "Should return store's id")
        store_id = response.value
        # check if it is impossible to open an already opened store
        response = self.service.open_store(good_register_info["username"], store_name)
        self.assertTrue(is_error(response), "store already exists")

    def open_store(self, username, stores_name):
        """
        Assumption: username already logged in
        """
        response = self.service.open_store(username, stores_name)
        self.assertTrue(not is_error(response))
        self.assertIsNotNone(response.value, "Should return store's id")
        return response.value

    def test_6_add_products_to_inventory(self):
        """
        II.4.1.1

        """
        self.login(good_register_info)
        username = good_register_info["username"]
        # open a store
        store_id = self.open_store(username, store_name)
        # assert the store is empty first
        self.__check_products_of_store(store_id, expected_products=[])
        # add a product
        response = self.service.add_new_product_to_inventory(username, store_id, **add_new_product_args)
        self.assertTrue(not is_error(response), f"{response.msg}")
        self.__check_products_of_store(store_id, expected_products=[default_product_name])

    def __check_products_of_store(self, store_id, expected_products):
        response = self.service.get_store_info(store_id)
        self.assertTrue(not is_error(response))
        self.assertTrue(response.value is not None)
        store_info = response.value
        # self.assertTrue(store_info["founder_id"] == guest_id)
        self.assertTrue(store_info["store_name"] == store_name)
        self.assertTrue(store_info["ID"] == store_id)
        self.assertEqual(expected_products, store_info["products"])

    # def test_7_edit_product_info(self):
    #     """
    #     II.4.1.3
    #     TODO
    #     """
    #     # response = service.edit_product_info(guest_id, store_id, product1_id, )
    #
    #     pass

    # def test_8_remove_products_from_inventory(self):
    #     """
    #     II.4.1.2
    #
    #     """
    #     self.login(good_register_info)
    #     username = good_register_info["username"]
    #     store_id = self.open_store(username, store_name)
    #     # add a new product
    #     response = self.service.add_products_to_inventory(username, store_id, product2_id, 1)
    #     self.assertTrue(not is_error(response))
    #     self.__check_products_of_store(store_id, expected_products=[default_product_name])
    #     # remove the product
    #     response = self.service.remove_products_from_inventory(username, store_id, product2_id, 1)
    #     self.assertTrue(not is_error(response))
    #     self.__check_products_of_store(store_id, expected_products=[])
    #     # same with more than 1 in quantity
    #     response = self.service.add_products_to_inventory(username, store_id, product2_id, 2)
    #     self.assertTrue(not is_error(response))
    #     self.__check_products_of_store(store_id, expected_products=[default_product_name] * 2)
    #     response = self.service.remove_products_from_inventory(username, store_id, product2_id, 1)
    #     self.assertTrue(not is_error(response))
    #     self.__check_products_of_store(store_id, expected_products=[default_product_name] * 1)

    """Guest's Purchase actions"""

    # def test_9_get_store_info(self):
    #     """
    #     II.2.1
    #     Tested in 'test_add_products_to_inventory'
    #     """
    #     pass
    #
    # def test_A1_search_product(self):
    #     """
    #     II.2.2
    #     TODO
    #     """
    #     pass

    def test_A2_add_product_to_shopping_cart(self):
        """
        II.2.3

        """
        g_id = self.enter_as_guest().value
        self.login(good_register_info2)  # store opener
        store_opener = good_register_info2["username"]
        store_id = self.open_store(store_opener, store_name)
        # add product that does'nt exist to shopping cart
        response = self.service.add_product_to_shopping_cart(g_id, store_id, product1_id, 1)
        self.assertTrue(is_error(response), "product does not exist in inventory")
        # add products to inventory
        p1_id, p2_id = self.add_products_to_inventory(store_id, store_opener)
        # add product to shopping cart - good
        response = self.service.add_product_to_shopping_cart(g_id, store_id, p1_id, 1)
        self.assertTrue(not is_error(response))

        # add the same product but no more products in inventory FIXME
        response = self.service.add_products_to_inventory(good_register_info2["username"], store_id, p1_id, 1)
        self.assertTrue(is_error(response), "there are no any products in the inventory")

        # bad add
        response = self.service.add_product_to_shopping_cart(g_id, store_id, p2_id, 2)
        self.assertTrue(is_error(response))

        # check in the shopping cart
        response = self.service.get_shopping_cart(g_id)
        self.assertTrue(not is_error(response))
        self.assertIsNotNone(response.value)
        cart = response.value.shopping_baskets
        basket = cart[store_id].get_products_and_quantities()
        self.assertTrue(basket[p1_id] == 1)
        self.assertTrue(p2_id not in basket)

    def add_products_to_inventory(self, store_id, store_opener):
        r1 = self.service.add_new_product_to_inventory(store_opener, store_id, **add_new_product_args)
        self.assertTrue(not is_error(r1))
        r2 = self.service.add_new_product_to_inventory(store_opener, store_id, **add_new_product_args)
        self.assertTrue(not is_error(r2))
        self.assertIsNotNone(r1.value)
        self.assertIsNotNone(r2.value)
        return r1, r2

    # def test_A3_get_shop_cart(self):
    #     """
    #     II.2.4
    #     Tested in 'test_add_product_to_shop_cart'
    #     """

    def test_A4_remove_product_from_shop_cart(self):
        """
        II.2.4

        """
        g_id = self.enter_as_guest().value
        self.login(good_register_info2)  # store opener
        store_id = self.open_store(good_register_info2["username"], store_name)
        store_opener = good_register_info2["username"]
        # add products to inventory
        p1_id, p2_id = self.add_products_to_inventory(store_id, store_opener)
        # add product to shopping cart
        response = self.service.add_product_to_shopping_cart(g_id, store_id, p1_id, 1)
        self.assertTrue(not is_error(response))
        # bad remove
        response = self.service.remove_product_from_shopping_cart(g_id,
                                                                  ProductPurchaseRequest(store_id, p2_id, 1))
        self.assertTrue(is_error(response))
        # good remove
        response = self.service.remove_product_from_shopping_cart(g_id,
                                                                  ProductPurchaseRequest(store_id, p1_id, 1))
        self.assertTrue(not is_error(response))

    # def test_A5_purchase_shop_cart(self):
    #     """
    #     II.2.5
    #     TODO: test product race condition, (test bad payment as well?)
    #     """
    #     g_id = self.enter_as_guest().value
    #     self.login(good_register_info2)  # store opener
    #     store_id = self.open_store(good_register_info2["username"], store_name)
    #
    #     service.add_product_to_shoppping_cart(guest_id, store_id, product1_id, 1)
    #     response = service.purchase_shopping_cart(guest_id, good_payment_info)
    #     self.assertTrue(not is_error(response))
    #     self.__check_products_of_store(expected_products=[])
    #     response = service.get_shopping_cart(guest_id)
    #     self.assertTrue(not is_error(response))
    #     self.assertIsNotNone(response.value)
    #     cart = response.value
    #     with self.assertRaises(KeyError):
    #         cart[store_id]

    # def test_A51_purchase_shop_cart(self):
    #     l = [0, 0]
    #
    #     def to_thread(id, payment, idx):
    #         r = service.purchase_shopping_cart(id, payment)
    #         l[idx] = r
    #
    #     """
    #     II.2.5
    #     rece condition
    #     """
    #
    #     import threading
    #     service.add_products_to_inventory(guest_id, store_id, product1_id, 1)
    #     guest2 = self.enter()
    #     guest3 = self.enter()
    #     service.add_product_to_shoppping_cart(guest2, store_id, product1_id, 1)
    #     service.add_product_to_shoppping_cart(guest3, store_id, product1_id, 1)
    #     thread1 = threading.Thread(target=to_thread, args=(guest2, good_payment_info, 0))
    #     thread2 = threading.Thread(target=to_thread, args=(guest3, good_payment_info, 1))
    #     thread1.start()
    #     thread2.start()
    #     # self.assertTrue((is_error(l[0]) and not is_error(l[1])) or (not is_error(l[0]) and is_error(l[1])))
    #
    # """Member's purchase actions"""
    #
    # def test_A6_logout(self):
    #     """
    #     II.3.1
    #
    #     """
    #     # prepare shopping cart
    #     response = service.add_products_to_inventory(guest_id, store_id, product1_id, 1)
    #     self.assertTrue(not is_error(response))
    #     response = service.add_product_to_shoppping_cart(guest_id, store_id, product1_id, 1)
    #     self.assertTrue(not is_error(response))
    #     # TODO finish
    #     pass
    #
    # def test_A7_exit(self):
    #     """
    #     II.1.2
    #
    #     """
    #
    #     pass
    #
    # # def test_review_product(self):
    # #     """
    # #     II.3.3
    # #
    # #     """
    # #     pass
    # #
    # # def test_grade_product(self):
    # #     """
    # #     II.3.4.1
    # #
    # #     """
    # #     pass
    # #
    # # def test_grade_store(self):
    # #     """
    # #     II.3.4.2
    # #
    # #     """
    # #     pass
    # #
    # # def test_contact_store(self):
    # #     """
    # #     II.3.5
    # #
    # #     """
    # #     pass
    # #
    # # def test_complaint(self):
    # #     """
    # #     II.3.6
    # #
    # #     """
    # #     pass
    # #
    # # def test_get_personal_purchase_history(self):
    # #     """
    # #     II.3.7
    # #
    # #     """
    # #     pass
    # #
    # # def test_get_personal_info(self):
    # #     """
    # #     II.3.8
    # #
    # #     """
    # #     pass
    # #
    # # def test_edit_personal_info(self):
    # #     """
    # #     II.3.8
    # #
    # #     """
    # #     pass
    # #
    # # def test_upgrade_member_security(self):
    # #     """
    # #     II.3.9
    # #
    # #     """
    # #     pass
    #
    # # def test_edit_store_policy(self):
    # #     """
    # #     II.4.2
    # #     *NOT*  need to implement to this version
    # #
    # #     """
    # #     pass
    # #
    # # def test_change_purchase_policy(self):
    # #     """
    # #     II.4.3.1
    # #
    # #     """
    # #     pass
    # #
    # # def test_change_discount_policy(self):
    # #     """
    # #     II.4.3.2
    # #
    # #     """
    # #     pass
    #
    # def test_A8_add_store_owner(self):
    #     """
    #     II.4.4
    #
    #     """
    #     # prepare new member
    #     new_owner_id = self.register_new_guest()
    #     # check precondition
    #     response = service.get_store_roles(guest_id, store_id)
    #     self.assertTrue(not is_error(response), "Should not be an error")
    #     self.assertIsNotNone(response.value)
    #     officials = response.value
    #     self.assertTrue(len(officials) == 1 and officials[guest_id])  # fooya!
    #     # test
    #     response = service.add_store_owner(guest_id, store_id, new_owner_id)
    #     self.assertTrue(not is_error(response), "Should not be an error")
    #     response = service.get_store_roles(guest_id, store_id)
    #     self.assertTrue(not is_error(response), "Should not be an error")
    #     self.assertIsNotNone(response.value)
    #     officials = response.value
    #     self.assertTrue(len(officials) == 2 and officials[guest_id] and officials[new_owner_id])  # bad! really bad
    #     pass
    #
    # # def test_remove_store_owner(self):
    # #     """
    # #     II.4.5
    # #
    # #     """
    # #     pass
    #
    # def test_A9_add_store_manager(self):
    #     """
    #     II.4.6
    #
    #     """
    #     global manager_id
    #     manager_id = self.register_new_guest()
    #     response = service.add_store_manager(guest_id, store_id, manager_id)
    #     self.assertTrue(not is_error(response), "Should not be an error")
    #     response = service.get_store_roles(guest_id, store_id)
    #     self.assertTrue(not is_error(response), "Should not be an error")
    #     self.assertIsNotNone(response.value)
    #     officials = response.value
    #     self.assertTrue(len(officials) == 3 and officials[guest_id] and officials[manager_id])  # Shema Israel
    #
    # def test_AA1_change_manager_permission(self):
    #     """
    #     II.4.7
    #     TODO
    #     """
    #     pass
    #
    # # def test_remove_store_manager(self):
    # #     """
    # #     II.4.8
    # #
    # #     """
    # #     pass
    #
    # def test_AA2_close_store(self):
    #     """
    #     II.4.9
    #
    #     """
    #     pass
    #
    # # def test_reopen_store(self):
    # #     """
    # #     II.4.10
    # #
    # #     """
    # #     pass
    #
    # def test_AA3_get_store_roles(self):
    #     """
    #     II.4.11
    #     Tested in 'test_add_store_owner'
    #     """
    #     pass
    #
    # # def test_get_users_messages(self):
    # #     """
    # #     II.4.12.1
    # #
    # #     """
    # #     pass
    # #
    # # def test_reply_users_messages(self):
    # #     """
    # #     II.4.12.2
    # #
    # #     """
    # #     pass
    #
    # def test_AA4_get_store_purchase_history(self):
    #     """
    #     II.4.13
    #
    #     """
    #     response = service.get_store_purchase_history(guest_id, store_id)
    #     self.assertTrue(not is_error(response))
    #     self.assertIsNotNone(response.value)
    #     purchase_history = response.value
    #     self.assertTrue(len(purchase_history) == 1)
    #     purchase = purchase_history[0]
    #     self.assertTrue(purchase.product_name == product1_name and purchase.quantity == 1)
    #
    # # def test_close_store_permanently(self):
    # #     """
    # #     II.6.1
    # #
    # #     """
    # #     pass
    # #
    # # def test_remove_member(self):
    # #     """
    # #     II.6.2
    # #
    # #     """
    # #     pass
    # #
    # # def test_get_all_users_messages_by_admin(self):
    # #     """
    # #     II.6.3.1
    # #
    # #     """
    # #     pass
    # #
    # # def test_reply_users_messages_by_admin(self):
    # #     """
    # #     II.6.3.2
    # #
    # #     """
    # #     pass
    #
    # def test_AA5_get_stores_purchase_history_by_admin(self):
    #     """
    #     II.6.4
    #     TODO
    #     """
    #     pass
    #
    # # def test_get_system_statistic_by_admin(self):
    # #     """
    # #     II.6.5
    # #
    # #     """
    # #     pass
    #
    # def enter(self):
    #     r = service.enter_as_guest()
    #     return r.value
    #
    # def register_new_guest(self):
    #     id = service.enter_as_guest().value
    #     service.register((id, {"username": "new", "password": "123"}))
    #     return id


if __name__ == '__main__':
    unittest.main()
