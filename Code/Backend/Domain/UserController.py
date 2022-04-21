from typing import Dict

from Code.Backend.Domain import MemberState
from Code.Backend.Domain.MFResponse import Response
from Code.Backend.Domain.Visitor import Visitor


class UserController:
    def __init__(self):
        """

        """
        self.__users: Dict[str, Visitor] = {}  # username: user
        self.__members: Dict[str, MemberState] = {}  # username: member
        self.__id_counter = 0

    def init(self):
        pass

    def create_guest(self):
        new_id = self.generate_id()
        user = Visitor(new_id)
        self.__users[new_id] = user
        return Response(value=new_id)

    def generate_id(self):
        self.__id_counter += 1
        return str(self.__id_counter)

    def exit(self, user_id: str):
        if user_id not in self.__users:
            return Response(msg="user does not exist")
        return self.__users[user_id].exit()

    def register(self, user_id: str, member_info: Dict):
        key = member_info["username"]
        if key in self.__members:
            return Response("username already exists")
        new_status = self.__users[user_id].register(member_info)
        if new_status.error_occurred():
            return new_status
        self.__members[key] = new_status.value
        return Response()


    def login(self, guest_id: str, username: str, password: str):
        if username not in self.__members:
            return Response(msg="username doesn't exist")
        if guest_id not in self.__users:
            return Response(msg="guest id doesn't exist")
        return self.__users[guest_id].login(self.__members[username], password)

    def is_logged_in(self, user_id: str):
        if user_id not in self.__users:
            return Response(msg="user")

    def is_member(self, user_id):
        if user_id not in self.__users:
            return Response("user doesn't exist")
        return self.__users[user_id].is_logged_in()

    def add_product_to_shop_cart(self, user_id: str, product_info):  # todo: shouldn't be shopping basket?
        if user_id not in self.__users:
            return Response.from_error("user doesn't exist")
        return self.__users[user_id].add_product_to_shopping_cart(product_info)

    def get_shop_cart(self, user_id: str):
        if user_id not in self.__users:
            return Response.from_error("user doesn't exist")
        return self.__users[user_id].get_shopping_cart()

    def remove_product_from_shop_cart(self, user_id: str, product_id: str): # todo: shouldn't be shopping basket?
        if user_id not in self.__users:
            return Response.from_error("user doesn't exist")
        return self.__users[user_id].remove_product_from_shopping_cart(product_id)

    def logout(self, user_id: str):
        if user_id not in self.__users:
            return Response.from_error("user doesn't exist")
        return self.__users[user_id].logout()

    def review_product(self, user_id: str, product_info, review: str):
        pass  # todo

    def grade_product(self, user_id: str, product_info: str, grade):
        pass  # todo

    def get_personal_purchase_history(self, user_id: str):
        pass  # todo

    def get_personal_info(self, user_id: str):
        pass  # todo

    def edit_personal_info(self, user_id: str, new_personal_info):
        pass  # todo


