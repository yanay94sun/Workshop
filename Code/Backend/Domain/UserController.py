from typing import Dict

from Code.Backend.Domain.MFResponse import Response
from Code.Backend.Domain.Visitor import Visitor


class UserController:
    def __init__(self):
        """

        """
        self.users: Dict[str, Visitor] = {}
        self.id_counter = 0

    def create_guest(self):
        id = self.generate_id()
        user = Visitor(id)
        self.users[id] = user
        return Response(value=id)

    def generate_id(self):
        self.id_counter += 1
        return str(self.id_counter)

    def exit(self, user_id: str):
        pass

    def register(self, guest_id: str, user_info):
        pass

    def login(self, guest_id: str, username: str, password: str):
        pass

    def is_logged_in(self, user_id: str):
        pass

    def add_product_to_shop_cart(self, user_id: str, product_info):
        pass

    def get_shop_cart(self, user_id: str):
        pass

    def remove_product_from_shop_cart(self, user_id: str, product_id: str):
        pass

    def logout(self, user_id: str):
        pass

    def review_product(self, user_id: str, product_info, review: str):
        pass

    def grade_product(self, user_id: str, product_info: str, grade):
        pass

    def get_personal_purchase_history(self, user_id: str):
        pass

    def get_personal_info(self, user_id: str):
        pass

    def edit_personal_info(self, user_id: str, new_personal_info):
        pass
