from Code.Backend.Domain import auth
from Code.Backend.Domain.DomainDataObjects.ProductPurchaseRequest import ProductPurchaseRequest
from Code.Backend.Domain.VisitorStates.GuestState import GuestState
from Code.Backend.Domain.VisitorStates.MemberState import MemberState
from Code.Backend.Domain.MFResponse import Response


class Visitor:
    """
    this class represents a user of the system
    """
    def __init__(self, uid: str):
        self.__id = uid
        self.__status = GuestState()

    def exit(self):
        return self.__status.exit()

    def login(self, member_state: MemberState, password: str):
        if self.is_logged_in():
            return Response.from_error("user is already logged in")
        if not member_state.password_confirmed(password):
            return Response.from_error("invalid password")
        self.__status = member_state
        return Response(member_state)

    def is_logged_in(self):
        return self.__status.is_logged_in()

    def logout(self):
        if not self.is_logged_in():
            return Response(msg="member is not logged in")
        logged_out_member = self.__status
        self.__status = GuestState()
        return Response(logged_out_member)

    def register(self, member_info) -> Response:
        """
        return the new state so the UC could save it
        """
        if self.is_logged_in():
            return Response.from_error("the user is already a member")
        # hashing pwd
        hashed_pwd = auth.hash(member_info["password"])
        # change pwd
        member_info["password"] = hashed_pwd
        ret = MemberState(self.__status.get_shopping_cart(), member_info)
        return Response(value=ret)

    def add_product_to_shopping_cart(self, product_info):
        return self.__status.add_product_to_shopping_cart(product_info)

    def get_shopping_cart(self):
        return self.__status.get_shopping_cart()

    def remove_product_from_shopping_cart(self, ppr: ProductPurchaseRequest):
        return self.__status.get_shopping_cart().remove_product(ppr)

    def get_username(self):
        return self.__status.get_username()