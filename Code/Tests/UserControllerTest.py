import unittest

from Code.Backend.Domain.Controllers.UserController import UserController
from Code.Backend.Domain.DomainDataObjects.ProductPurchaseRequest import ProductPurchaseRequest



class UserControllerTests(unittest.TestCase):
    def setUp(self):
        self.uc = UserController()
        self.visitor1_id = self.uc.create_guest().value
        self.visitor2_id = self.uc.create_guest().value
        self.uc.register(self.visitor1_id, {"username": "v1", "password": "11"})
        self.uc.login(self.visitor1_id, "v1", "11")

    def test_enter_as_guest(self):
        new_id = self.uc.create_guest()
        self.assertTrue(new_id != self.visitor1_id and new_id != self.visitor2_id, "different guests got the same id")

    def test_exit(self):
        res1 = self.uc.exit(self.visitor1_id)
        res2 = self.uc.exit(self.visitor2_id)
        self.assertFalse(res1.error_occurred(), res1.msg)
        self.assertFalse(res2.error_occurred(), res2.msg)

    def test_register(self):
        res = self.uc.register(self.visitor2_id, {"username": "v1", "password": "11"})
        self.assertTrue(res.error_occurred(), "error didn't occurred while registering same username")
        res = self.uc.register(self.visitor1_id, {"username": "v1", "password": "11"})
        self.assertTrue(res.error_occurred(), "error didn't occurred while registering user twice")
        res = self.uc.register(self.visitor2_id, {"username": "v2", "password": "11"})
        self.assertFalse(res.error_occurred(), "error occurred in legit register")

    def test_login(self):
        res = self.uc.login(self.visitor1_id, "v1", "11")
        self.assertTrue(res.error_occurred(), "user can't login twice")
        res = self.uc.login(self.visitor2_id, "v2", "11")
        self.assertTrue(res.error_occurred(), "login unregistered user")
        self.uc.register(self.visitor2_id, {"username": "v2", "password": "11"})
        self.uc.logout(self.visitor2_id)
        res = self.uc.login(self.visitor1_id, "v2", "11")
        self.assertTrue(res.error_occurred(), "user was already logged in to another member")
        res = self.uc.login(self.visitor2_id, "v2", "12")
        self.assertTrue(res.error_occurred(), "invalid password was valid!")
        res = self.uc.login(self.visitor2_id, "v2", "11")
        self.assertFalse(res.error_occurred(), res.msg)


    def test_add_product_to_shop_cart(self):
        """
        II.2.3

        """
        ppr = ProductPurchaseRequest("s1", "p1", 10)
        res = self.uc.add_product_to_shop_cart(self.visitor2_id, ppr)
        self.assertFalse(res.error_occurred(), res.msg)
        res = self.uc.get_shopping_cart(self.visitor2_id)
        self.assertFalse(res.error_occurred(), res.msg)
        prdct = list(res.value.iter_products())[0]
        self.assertTrue(prdct.product_id == ppr.product_id, "got unknown product id from basket")

    def test_get_shopping_cart(self):
        """
        II.2.4

        """
        ppr = ProductPurchaseRequest("s1", "p1", 10)
        res1 = self.uc.add_product_to_shop_cart(self.visitor1_id, ppr)
        self.assertFalse(res1.error_occurred(), res1.msg)
        res = self.uc.get_shopping_cart(self.visitor2_id)
        self.assertFalse(res.error_occurred(), res.msg)
        self.assertTrue(len(res.value.shopping_baskets) == 0, "shopping cart had somthing whiel it shuoldnt")
        res = self.uc.get_shopping_cart(self.visitor1_id)
        self.assertFalse(res.error_occurred(), res.msg)
        self.assertTrue(len(res.value.shopping_baskets) == 1, f"added single ppr got {len(res.value.shopping_baskets)} baskets")



    def test_remove_product_from_shop_cart(self):
        """
        II.2.4

        """
        ppr = ProductPurchaseRequest("s1", "p1", 10)
        res1 = self.uc.add_product_to_shop_cart(self.visitor1_id, ppr)
        self.assertFalse(res1.error_occurred(), res1.msg)
        res = self.uc.remove_product_from_shopping_cart(self.visitor2_id, ppr)
        self.assertTrue(res.error_occurred(), "removed product from user who doesnt have it")
        res = self.uc.remove_product_from_shopping_cart(self.visitor1_id, ppr)
        self.assertFalse(res.error_occurred(), res.msg)
        res = self.uc.remove_product_from_shopping_cart(self.visitor1_id, ppr)
        self.assertTrue(res.error_occurred(), "ppr already removed from shopping cart")


    def test_logout(self):
        """
        II.3.1

        """
        res = self.uc.logout(self.visitor2_id)
        self.assertTrue(res.error_occurred(), "succeeded logging out unregistered user")
        res = self.uc.logout(self.visitor1_id)
        self.assertFalse(res.error_occurred(), res.msg)
        res = self.uc.logout(self.visitor1_id)
        self.assertTrue(res.error_occurred(), "succeeded logging out unregistered user")



if __name__ == '__main__':
    unittest.main()
