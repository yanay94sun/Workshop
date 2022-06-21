import unittest

from Code.Backend.Domain.Controllers.StoreController import StoreController
from Code.Backend.Domain.Controllers.UserController import UserController
from Code.Backend.Domain.Facade import Facade
from Code.Backend.Domain.Publisher.NotificationController import NotificationController, Activities
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
        self.nc.register_store(sid, username)
        ################################

        # self.nc.subscribe(username, sid, Activities.PURCHASE_IN_STORE)

        self.uc.logout(uid)
        self.nc.notify_all(sid, Activities.PURCHASE_IN_STORE, "test msg")

        self.uc.login(uid, username, "123")
        msg_from_user = self.uc.pull_user_msgs(uid)
        self.assertEqual(msg_from_user[0], "test msg")

    def test_unsubscribe_manually(self):
        uid1 = self.uc.create_guest().value
        uid2 = self.uc.create_guest().value
        username1 = "m1"
        username2 = "m2"
        sid = "The_Store"
        self.uc.register(uid1, {"username": username1, "password": "123"})
        self.uc.register(uid2, {"username": username2, "password": "123"})
        self.uc.login(uid1, username1, "123")
        self.sc.open_store(username1, sid)

        # should be inside the openstore
        self.nc.register_store(sid, username1)
        ################################

        self.nc.subscribe(username2, sid, Activities.PURCHASE_IN_STORE)

        self.uc.logout(uid1)
        self.nc.notify_all(sid, Activities.PURCHASE_IN_STORE, "test msg1")

        self.nc.unsubscribe(username2, sid, Activities.PURCHASE_IN_STORE)

        self.nc.notify_all(sid, Activities.PURCHASE_IN_STORE, "test msg2")

        self.uc.login(uid1, username1, "123")
        self.uc.login(uid2, username2, "123")

        msg_from_user1 = self.uc.pull_user_msgs(uid1)
        msg_from_user2 = self.uc.pull_user_msgs(uid2)
        self.assertEqual(len(msg_from_user1), 2)
        self.assertEqual(len(msg_from_user2), 1)

