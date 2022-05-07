# from plistlib import Dict
from Code.Backend.Domain.ShoppingCart import ShoppingCart
from Code.Backend.Domain.VisitorStates.VisitorState import State


class MemberState(State):
    """

    """
    def __init__(self, shopping_cart: ShoppingCart, member_info):
        State.__init__(self, shopping_cart)
        self.__username = member_info["username"]
        self.__password = member_info["password"]
        self.__member_info = member_info

    def is_logged_in(self):
        return True

    def password_confirmed(self, password: str) -> bool:
        return self.__password == password



