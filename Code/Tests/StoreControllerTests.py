import unittest

from Code.Backend.Domain.Controllers.StoreController import StoreController
from Code.Backend.Domain.ShoppingBasket import ShoppingBasket
from Code.Backend.Domain.StoreOfficials.Permissions import Actions, Permissions
from Code.Backend.Domain.StoreOfficials.StoreFounder import StoreFounder

USER_ID = '123'
STORE_ID = '1'
PRODUCT_ID = "1"


class StoreControllerTests(unittest.TestCase):

    def setUp(self) -> None:
        self.sc = StoreController()

    def test_get_store_info(self):
        self.sc.open_store(USER_ID, "The_Store")
        response = self.sc.get_store_info("2")
        # ID does not exists
        self.assertEqual(response.msg, "Store id does not exist or is inactive")
        # ID exists
        response = self.sc.get_store_info("1")
        self.assertTrue(response.value is not None)

    def test_get_stores_info(self):
        response = self.sc.get_stores_info()
        self.assertEqual(response.msg, "No stores in the System")
        self.sc.open_store(USER_ID, "The_Store")
        response = self.sc.get_stores_info()
        # should be a store in the system
        self.assertTrue(len(response.value) == 1)
        self.sc.open_store(USER_ID, "The_second_Store")
        response = self.sc.get_stores_info()
        # should be 2 stores in the system
        self.assertTrue(len(response.value) == 2)

    def test_open_store(self):
        self.sc.open_store(USER_ID, "The_Store")
        response = self.sc.open_store(USER_ID, "The_Store")
        # can not create store with a name that is in the system
        self.assertEqual(response.msg, "Store name already exists")
        # new name
        response = self.sc.open_store(USER_ID, "The_Store2")
        self.assertTrue(len(response.value) == 1)

    def test_add_products_to_inventory(self):
        self.sc.open_store(USER_ID, "The_Store")
        # create new product
        response = self.sc.add_new_product_to_inventory(USER_ID, STORE_ID, "Apple", "cool apple", 30, "fruits")
        self.assertEqual(response.value, PRODUCT_ID)
        # add more quantity
        self.sc.add_products_to_inventory(USER_ID, STORE_ID, PRODUCT_ID, 9)
        # check if the amount is really 9 as it should be
        self.assertTrue(self.sc.get_product(STORE_ID, PRODUCT_ID, 9) is not None)
        self.assertTrue(self.sc.get_product(STORE_ID, PRODUCT_ID, 10) is None)

    def test_remove_products_from_inventory(self):
        self.sc.open_store(USER_ID, "The_Store")
        self.sc.add_new_product_to_inventory(USER_ID, STORE_ID, "Apple", "cool apple", 30, "fruits")
        self.sc.add_products_to_inventory(USER_ID, STORE_ID, PRODUCT_ID, 9)
        self.sc.remove_products_from_inventory(USER_ID, STORE_ID, PRODUCT_ID, 3)

        # should be 6 products now
        self.assertTrue(self.sc.get_product(STORE_ID, PRODUCT_ID, 6) is not None)
        self.assertTrue(self.sc.get_product(STORE_ID, PRODUCT_ID, 7) is None)
        # remove more products than possible
        response = self.sc.remove_products_from_inventory(USER_ID, STORE_ID, PRODUCT_ID, 7)

        self.assertEqual(response.msg, "Attempt to remove more Items then the existing quantity")
        # quantity should not change
        self.assertTrue(self.sc.get_product(STORE_ID, PRODUCT_ID, 6) is not None)
        self.assertTrue(self.sc.get_product(STORE_ID, PRODUCT_ID, 7) is None)

    def test_edit_product_info(self):
        self.sc.open_store(USER_ID, "The_Store")
        self.sc.add_new_product_to_inventory(USER_ID, STORE_ID, "Apple", "Cool apple", 30, "Fruits")
        response = self.sc.edit_product_info(USER_ID, STORE_ID, PRODUCT_ID, name="Apple-Juice", description=None,
                                             rating=None
                                             , price=None, category=None)
        self.assertEqual(response.value, "Product was edited")
        self.assertTrue(self.sc.get_product(STORE_ID, PRODUCT_ID, 0).get_name() == "Apple-Juice")

        response = self.sc.edit_product_info(USER_ID, STORE_ID, PRODUCT_ID, name=None, category="Juice", rating=None
                                             , price=None, description=None)
        self.assertEqual(response.value, "Product was edited")
        self.assertEqual(self.sc.get_product(STORE_ID, PRODUCT_ID, 0).get_category(), "Juice")

        response = self.sc.edit_product_info(USER_ID, STORE_ID, PRODUCT_ID, price=50, name=None, category=None,
                                             rating=None
                                             , description="Cool Juice")
        self.assertEqual(response.value, "Product was edited")
        self.assertEqual(self.sc.get_product(STORE_ID, PRODUCT_ID, 0).get_price(), 50)
        self.assertEqual(self.sc.get_product(STORE_ID, PRODUCT_ID, 0).get_description(), "Cool Juice")

    def test_search_product(self):
        self.sc.open_store(USER_ID, "The_Store")
        self.sc.add_new_product_to_inventory(USER_ID, STORE_ID, "Apple", "Cool apple", 30, "Fruits")
        response = self.sc.search_product("Apple", by_name=True, by_category=None, filter_type=None, filter_value=None)
        self.assertEqual(response.value[0].get_name(), "Apple")
        response = self.sc.search_product("Fruits", by_name=True, by_category=True, filter_type=None, filter_value=None)
        self.assertEqual(response.value[0].get_category(), "Fruits")
        # products does not exists
        response = self.sc.search_product("bla bla", by_name=True, by_category=None, filter_type=None,
                                          filter_value=None)
        self.assertTrue(len(response.value) == 0)

    def test_add_store_owner(self):
        self.sc.open_store(USER_ID, "The_Store")
        new_user_id = '111'
        response = self.sc.add_store_owner(USER_ID, STORE_ID, new_user_id)
        self.assertEqual(response.value, "Made User with id: 111 an owner")
        response = self.sc.add_store_owner(USER_ID, STORE_ID, USER_ID)
        # can not add store owner that is already store owner
        self.assertEqual(response.msg, "User is already an Owner of this store")

    def test_add_store_manager(self):
        self.sc.open_store(USER_ID, "The_Store")
        new_user_id = '111'
        response = self.sc.add_store_manager(USER_ID, STORE_ID, new_user_id)
        self.assertEqual(response.value, "Made User with id: 111 a manager")
        response = self.sc.add_store_owner(USER_ID, STORE_ID, USER_ID)
        # can not add store owner that is already store owner
        self.assertTrue(response.msg, "User is already a Manager of this store")

    def test_change_manager_permission(self):
        self.sc.open_store(USER_ID, "The_Store")
        self.sc.add_new_product_to_inventory(USER_ID, STORE_ID, "Apple", "Cool apple", 30, "Fruits")
        manager_id = '111'
        self.sc.add_store_manager(USER_ID, STORE_ID, manager_id)
        # user should not be able to change inventory
        response = self.sc.add_products_to_inventory(manager_id, STORE_ID, PRODUCT_ID, 3)
        self.assertEqual(response.msg, "User does not have access to this action")
        new_per = {1: True, 2: False, 3: False, 4: False, 5: False, 6: False, 7: False}
        response = self.sc.change_manager_permission(USER_ID, STORE_ID, manager_id, new_per)
        self.assertEqual(response.value, "Permissions successfully changed")
        # should have access
        response = self.sc.add_products_to_inventory(manager_id, STORE_ID, PRODUCT_ID, 3)
        self.assertEqual(response.value, "Added 3 items of Apple")

    def test_get_store_roles(self):
        self.sc.open_store(USER_ID, "The_Store")
        manager_id = '111'
        self.sc.add_store_manager(USER_ID, STORE_ID, manager_id)
        response = self.sc.get_store_roles(USER_ID, STORE_ID)
        self.assertTrue(response.value is not None)
        # check if user with id 123 is an owner
        self.assertTrue(isinstance(response.value[USER_ID], StoreFounder))

    def test_get_store_purchase_history(self):
        pass

    def test_get_basket_price(self):
        self.sc.open_store(USER_ID, "The_Store")
        self.sc.add_new_product_to_inventory(USER_ID, STORE_ID, "Apple", "cool apple", 50, "Fruits")
        self.sc.add_products_to_inventory(USER_ID, STORE_ID, PRODUCT_ID, 9)
        basket = ShoppingBasket(STORE_ID)
        basket.add_to_basket(PRODUCT_ID, 3)
        discount1 = self.sc.add_visible_discount(STORE_ID, [], 0.4, "24/5/2022", by_category="Fruits").value.get_id()
        discount2 = self.sc.add_conditional_discount(STORE_ID, [PRODUCT_ID], 0.3, "24/5/2022", {PRODUCT_ID: 2},
                                                     0).value.get_id()
        discount3 = self.sc.add_and_discount(STORE_ID, discount1, discount2).value.get_id()
        response = self.sc.get_basket_price(STORE_ID, basket)
        self.assertEqual(response.value, 90)

        self.sc.add_new_product_to_inventory(USER_ID, STORE_ID, "Orange", "cool Orange", 30, "Fruits")
        self.sc.add_products_to_inventory(USER_ID, STORE_ID, "2", 9)
        basket.add_to_basket("2", 5)

        discount4 = self.sc.add_conditional_discount(STORE_ID, ["2"], 0.2, "bla", {"2": 2}).value.get_id()
        self.sc.add_or_discount(STORE_ID, discount3, discount4)
        response = self.sc.get_basket_price(STORE_ID, basket)
        self.assertEqual(response.value, 180)

    def test_get_users_stores(self):
        self.sc.open_store(USER_ID, "The_Store")
        manager_id = '111'
        self.sc.add_store_manager(USER_ID, STORE_ID, manager_id)
        response = self.sc.get_officials_stores(USER_ID)
        self.assertTrue(response.value["1"] == 'The_Store')
        response = self.sc.get_officials_stores(manager_id)
        self.assertTrue(response.value["1"] == 'The_Store')

    def test_check_purchase_policy(self):
        self.sc.open_store(USER_ID, "The_Store")
        self.sc.add_new_product_to_inventory(USER_ID, STORE_ID, "Apple", "cool apple", 50, "Fruits")
        self.sc.add_products_to_inventory(USER_ID, STORE_ID, PRODUCT_ID, 9)
        basket = ShoppingBasket(STORE_ID)
        basket.add_to_basket(PRODUCT_ID, 3)

        rule1 = self.sc.add_simple_purchase_rule(STORE_ID, {PRODUCT_ID: 50}).value.get_id()
        rule2 = self.sc.add_simple_purchase_rule(STORE_ID, {}, min_price_to_have_for_purchase=50).value.get_id()
        self.sc.add_or_purchase_rule(STORE_ID, rule1, rule2)
        response = self.sc.check_purchase_policy(STORE_ID, basket)
        self.assertTrue(response.value)

        self.sc.add_simple_purchase_rule(STORE_ID,{}, by_category="PlayStation")
        response = self.sc.check_purchase_policy(STORE_ID,basket)
        self.assertTrue(not response.value)

    def test_close_store(self):
        self.sc.open_store(USER_ID, "The_Store")
        response = self.sc.close_store(USER_ID, STORE_ID)
        self.assertTrue(response.value == "Store was successfully closed")
        response = self.sc.get_store_info(STORE_ID)
        self.assertTrue(response.msg == "Store id does not exist or is inactive")

    def test_a_15_remove_store_owner(self):
        sc.open_store("123", "1")
        sc.add_store_owner("123", "1", "123456789")
        sc.add_store_owner("123", "1", "1234")
        sc.add_store_owner("1234", "1", "12345")
        sc.add_store_owner("1234", "1", "12346")
        sc.add_store_owner("12345", "1", "123456")
        sc.add_store_owner("123456", "1", "1234567")

        self.assertEqual(len(sc.stores["1"].get_officials()), 7)

        sc.remove_store_owner("123", "1", "1234")

        self.assertEqual(len(sc.stores["1"].get_officials()), 2)




if __name__ == '__main__':
    unittest.main()
