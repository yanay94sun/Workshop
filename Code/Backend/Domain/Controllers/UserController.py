from typing import Dict, List

from Code.Backend.Domain.ShoppingBasket import ShoppingBasket
from Code.Backend.Domain.ShoppingCart import ShoppingCart
from Code.Backend.Domain.VisitorStates.MemberState import MemberState
from Code.Backend.Domain.DomainDataObjects.ProductPurchaseRequest import ProductPurchaseRequest
from Code.Backend.Domain.MFResponse import Response
from Code.Backend.Domain.Visitor import Visitor
import Code.DAL.main as dal


class UserController:
    def __init__(self):
        """

        """
        self.__users: Dict[str, Visitor] = {}  # ip or other user identifier: user todo
        self.__members: Dict[str, MemberState] = {}  # username: member
        # self.__online_members = set()  # we can use as dictionary with timestamp to set online validity
        #                                # and clear it from time to time
        self.__online_members: Dict[MemberState, str] = {}  # Member: uid
        self.__id_counter = 0
        self.get_from_db()

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
        new_member = self.__users[user_id].register(member_info)
        if new_member.error_occurred():
            return new_member
        self.__members[key] = new_member.value
        return Response()

    def login(self, user_id: str, username: str, password: str):
        if username not in self.__members:
            return Response(msg="username doesn't exist")
        if user_id not in self.__users:
            return Response(msg="guest id doesn't exist")
        res = self.__users[user_id].login(self.__members[username], password)
        if not res.error_occurred():
            self.__online_members[res.value] = user_id
        return res

    def is_logged_in(self, user_id: str):
        if user_id not in self.__users:
            return Response(msg="user isn't logged in")
        return Response(value=self.__users[user_id].is_logged_in())

    def is_member(self, member_id):
        return member_id in self.__members

    def get_users_username(self, user_id):
        res = self.is_logged_in(user_id)
        if res.error_occurred():
            return res
        try:
            return Response(self.__users[user_id].get_username())
        except Exception as e:
            return Response.from_error(e.args[0])

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
        res = self.__users[user_id].logout()
        if not res.error_occurred():
            self.__online_members.pop(res.value)
        return res

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

    def is_online(self, username):
        if username not in self.__members:
            return Response.from_error(f"member {username} does not exist in the context for some reason")
        return self.__members[username] in self.__online_members

    def add_message_to_member(self, username, message):
        if username not in self.__members:
            return Response.from_error(f"member {username} does not exist in the context for some reason")
        self.__members[username].add_message(message)
        return Response()

    def pull_user_msgs(self, uid):
        username = self.__users[uid].get_username()
        return self.__members[username].pull_msgs()

    def remove_member(self, member_id):
        """
        call function only if checked that admin is using this
        member_id is username
        """
        if member_id in self.__members.keys():
            del self.__members[member_id]
            return Response(value='Removed member: ' + member_id)
        return Response(msg='member does not exist')

    def get_username_uid(self, username):
        return self.__online_members[self.__members[username]]

    def is_connected(self, user_id):
        if user_id in self.__users.keys():
            return Response(value=True)
        return Response(value=False)

    def get_from_db(self):
        users = dal.get_all_users()
        for user in users:
            username = user.user.username
            password = user.user.password

            cart: Dict[str, ShoppingBasket] = {}  # store_id, List[product, quantity]
            for basket in user.shopping_cart:
                sid = basket.store_id
                if sid not in cart:
                    cart[sid] = ShoppingBasket(sid)
                cart[sid].add_to_basket(str(basket.product_id), basket.quantity)
            shopping_cart = ShoppingCart()
            shopping_cart.shopping_baskets = cart

            member = MemberState(shopping_cart, {"username": username, "password": password})
            [member.add_message(n.message) for n in user.notifications]

            self.__members[username] = member



