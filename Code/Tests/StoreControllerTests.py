import unittest

from Code.Backend.Domain.Actions import Actions
from Code.Backend.Domain.DomainDataObjects.ProductPurchaseRequest import ProductPurchaseRequest
from Code.Backend.Domain.Controllers.StoreController import StoreController

sc = StoreController()
USER_ID = '123'
STORE_ID = '1'
PRODUCT_ID = "13"


class StoreControllerTests(unittest.TestCase):

    def test_1_get_store_info(self):
        sc.open_store(USER_ID, "The_Store")
        response = sc.get_store_info("2")
        # ID does not exists
        self.assertTrue(response.msg is not None)
        # ID exists
        response = sc.get_store_info("1")
        print(response.value)
        self.assertTrue(response.value is not None)

    def test_2_get_stores_info(self):
        response = sc.get_stores_info()
        # should be a store in the system
        self.assertTrue(response.value is not None)

    def test_3_open_store(self):
        response = sc.open_store("123", "The_Store")
        # can not create store with a name that is in the system
        self.assertTrue(response.msg is not None)
        # new name
        response = sc.open_store("123", "The_Store2")
        self.assertTrue(response.value is not None)

    def test_4_add_products_to_inventory(self):
        # create new product
        response = sc.add_products_to_inventory(USER_ID, STORE_ID, PRODUCT_ID, 4)
        self.assertTrue(response.value is not None)
        # add the more quantity
        sc.add_products_to_inventory(USER_ID, STORE_ID, PRODUCT_ID, 5)
        # check if the amount is really 9 as it should be
        self.assertTrue(sc.get_product(STORE_ID, PRODUCT_ID, 9) is not None)
        self.assertTrue(sc.get_product(STORE_ID, PRODUCT_ID, 10) is None)

    def test_5_remove_products_from_inventory(self):
        sc.remove_products_from_inventory(USER_ID, STORE_ID, PRODUCT_ID, 3)

        # should be 6 products now
        self.assertTrue(sc.get_product(STORE_ID, PRODUCT_ID, 6) is not None)
        self.assertTrue(sc.get_product(STORE_ID, PRODUCT_ID, 7) is None)
        # remove more products than possible
        response = sc.remove_products_from_inventory(USER_ID, STORE_ID, PRODUCT_ID, 7)

        self.assertTrue(response.msg == "Attempt to remove more Items then the existing quantity")
        # quantity should not change
        self.assertTrue(sc.get_product(STORE_ID, PRODUCT_ID, 6) is not None)
        self.assertTrue(sc.get_product(STORE_ID, PRODUCT_ID, 7) is None)

    def test_6_edit_product_info(self):
        response = sc.edit_product_info(USER_ID, STORE_ID, PRODUCT_ID, ProductPurchaseRequest(name="Apple"))
        self.assertTrue(response.value == "Product was edited")
        self.assertTrue(sc.get_product(STORE_ID, PRODUCT_ID, 0).get_name() == "Apple")
        response = sc.edit_product_info(USER_ID, STORE_ID, PRODUCT_ID, ProductPurchaseRequest(category="Fruits"))
        self.assertTrue(response.value == "Product was edited")
        self.assertTrue(sc.get_product(STORE_ID, PRODUCT_ID, 0).get_category() == "Fruits")

    def test_7_search_product(self):
        response = sc.search_product("Apple")
        self.assertTrue(response.value[0].get_name() == "Apple")
        response = sc.search_product("Fruits", by_category=True)
        self.assertTrue(response.value[0].get_category() == "Fruits")
        # products does not exists
        response = sc.search_product("bla bla")
        self.assertTrue(len(response.value) == 0)

    def test_8_add_store_owner(self):
        new_user_id = '111'
        response = sc.add_store_owner(USER_ID, STORE_ID, new_user_id)
        self.assertTrue(response.value is not None)
        response = sc.add_store_owner(USER_ID, STORE_ID, USER_ID)
        # can not add store owner that is already store owner
        self.assertTrue(response.msg is not None)

    def test_9_add_store_manager(self):
        new_user_id = '222'
        response = sc.add_store_manager(USER_ID, STORE_ID, new_user_id)
        self.assertTrue(response.value is not None)
        response = sc.add_store_owner(USER_ID, STORE_ID, USER_ID)
        # can not add store owner that is already store owner
        self.assertTrue(response.msg is not None)

    def test_a_10_change_manager_permission(self):
        response = sc.change_manager_permission(USER_ID, STORE_ID, '222', Actions.INVENTORY_ACTION, val=False)
        self.assertTrue(response.value == "Permissions successfully changed")
        response = sc.add_products_to_inventory('222', STORE_ID, PRODUCT_ID, 3)
        # user should not be able to change inventory
        self.assertTrue(response.msg is not None)

    def test_a_11_get_store_roles(self):
        response = sc.get_store_roles(USER_ID, STORE_ID)
        self.assertTrue(response.value is not None)
        # check if user with id 123 is an owner
        self.assertTrue(response.value[USER_ID].get_is_owner())

    def test_a_12_get_store_purchase_history(self):
        response = sc.get_store_purchase_history(USER_ID,STORE_ID)
        self.assertTrue(response.value is not None)
        # check if there is a purchase with 3 items
        self.assertTrue(response.value[0].quantity == 3)

    def test_a_13_close_store(self):
        response = sc.close_store(USER_ID, STORE_ID)
        self.assertTrue(response.value == "Store was successfully closed")
        response = sc.get_store_info(STORE_ID)
        self.assertTrue(response.msg == "Store id does not exist or is inactive")


if __name__ == '__main__':
    unittest.main()
