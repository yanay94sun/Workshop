import unittest

from Code.Backend.Domain.StoreController import StoreController

sc = StoreController()


class StoreControllerTests(unittest.TestCase):

    def setUp(self):
        sc.open_store("123", "The_Store")

    def test_get_store_info(self):
        response = sc.get_store_info("2")
        self.assertTrue(response.msg is not None)
        response = sc.get_store_info("1")
        self.assertTrue(response.value is not None)

    def test_get_stores_info(self):
        response = sc.get_stores_info()
        self.assertTrue(response.value is not None)

    def test_open_store(self):
        response = sc.open_store("123", "The_Store")
        self.assertTrue(response.msg is not None)
        response = sc.open_store("123", "The_Store2")
        self.assertTrue(response.value is not None)


if __name__ == '__main__':
    unittest.main()
