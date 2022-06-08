import unittest

from Code.Backend.Domain.Controllers.StoreController import StoreController
from Code.Backend.Domain.Controllers.UserController import UserController
from Code.Backend.Domain.Publisher.NotificationController import NotificationController
from Code.Backend.Domain.ShoppingBasket import ShoppingBasket
from Code.Backend.Domain.StoreOfficials.Permissions import Actions, Permissions
from Code.Backend.Domain.StoreOfficials.StoreFounder import StoreFounder



class NotificationDomainTests(unittest.TestCase):

    def setUp(self) -> None:
        self.sc = StoreController()
        self.uc = UserController()
        self.nc = NotificationController(self.uc)


    def test_subscribe_manually(self):
        uid = self.uc.create_guest().value
        username = "m1"
        sid = "The_Store"
        self.uc.register(uid, {"username": username, "password": "123"})
        self.uc.login(uid, username, "123")
        self.sc.open_store(username, sid)

        # should be inside the openstore
        self.nc.register_store(sid)
        ################################

        self.nc.subscribe(username, sid, 1)

        self.uc.logout(uid)
        self.nc.notify_all(sid, 1, "test msg")

        self.uc.login(uid, username, "123")
        msg_from_user = self.uc.pull_user_msgs(uid)
        self.assertEqual(msg_from_user[0], "test msg")

