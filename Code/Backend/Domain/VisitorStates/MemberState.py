# from plistlib import Dict
from passlib.exc import UnknownHashError

from Code.Backend.Domain import auth
from Code.Backend.Domain.ShoppingCart import ShoppingCart
from Code.Backend.Domain.VisitorStates.VisitorState import State

#import Code.DAL.main as dal
from Code.DAL.Objects.user import UserBase

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
        self.__waiting_messages = []
        self.__member_info = member_info
        dal_user = UserBase(**member_info)
        dal.persist_user(dal_user)

    def is_logged_in(self):
        return True

    # # TODO yanay changed to hashing verfy
    def password_confirmed(self, password: str) -> bool:
        return auth.verify(password, self.__password)

    # def password_confirmed(self, plain_password):
    #     try:
    #         return pwd_context.verify(plain_password, self.__password)
    #     except UnknownHashError:
    #         return False

    def get_username(self):
        return self.__username

    def add_message(self, msg):
        self.__waiting_messages.append(msg)

    def pull_msgs(self):
        tmp = self.__waiting_messages
        self.__waiting_messages = []
        return tmp

    def add_product_to_shopping_cart(self, product_info):
        super().add_product_to_shopping_cart(product_info)
        # persist




