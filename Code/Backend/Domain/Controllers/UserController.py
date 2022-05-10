from typing import Dict

from Code.Backend.Domain.VisitorStates import MemberState
from Code.Backend.Domain.DomainDataObjects.ProductPurchaseRequest import ProductPurchaseRequest
from Code.Backend.Domain.MFResponse import Response
from Code.Backend.Domain.Visitor import Visitor


class UserController:
    def __init__(self):
        """

        """
        self.__users: Dict[str, Visitor] = {}  # ip or other user identifier: user todo
        self.__members: Dict[str, MemberState] = {}  # username: member
        self.__id_counter = 0

    def init(self):
        pass

    def create_guest(self):
        new_id = self.__generate_id()
        user = Visitor(new_id)
        self.__users[new_id] = user
        return Response(value=new_id)

    def __generate_id(self):
        self.__id_counter += 1
        return str(self.__id_counter)

    def exit(self, user_id: str):
        if user_id not in self.__users:
            return Response(msg="user does not exist")
        return Response(self.__users[user_id].exit())

    def register(self, user_id: str, member_info: Dict):
        key = member_info["username"]
        if key in self.__members:
            return Response.from_error("username already exists")
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
            return Response(msg="user isn't logged in")
        return self.__users[user_id].is_logged_in()

    def is_member(self, member_id):
        return Response(member_id in self.__members)

    def get_users_username(self, user_id):
        res = self.is_logged_in(user_id)
        if res.error_occurred():
            return res

        return self.__users[user_id].get_username()

    def add_product_to_shop_cart(self, user_id: str, ppr: ProductPurchaseRequest):
        if user_id not in self.__users:
            return Response.from_error("user doesn't exist")
        return Response(self.__users[user_id].add_product_to_shopping_cart(ppr))

    def get_shopping_cart(self, user_id: str) -> Response:
        if user_id not in self.__users:
            return Response.from_error("user doesn't exist")
        return Response(self.__users[user_id].get_shopping_cart())

    def remove_product_from_shopping_cart(self, user_id: str, ppr: ProductPurchaseRequest):
        if user_id not in self.__users:
            return Response.from_error("user doesn't exist")
        return self.__users[user_id].remove_product_from_shopping_cart(ppr)

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


