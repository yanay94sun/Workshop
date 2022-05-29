# from plistlib import Dict
from Code.Backend.Domain.ShoppingCart import ShoppingCart
from Code.Backend.Domain.VisitorStates.VisitorState import State

from passlib.context import CryptContext

# hashing passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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

    # # TODO yanay changed to hashing verfy
    # def password_confirmed(self, password: str) -> bool:
    #     return self.__password == password

    def password_confirmed(self, plain_password):
        return pwd_context.verify(plain_password, self.__password)


    def get_username(self):
        return self.__username



