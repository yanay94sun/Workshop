from Code.Backend.Domain.GuestState import GuestState
from Code.Backend.Domain.MemberState import MemberState
from Code.Backend.Domain.ShoppingCart import ShoppingCart
from Code.Backend.Domain.State import State


class Visitor:
    def __init__(self, id: str):
        """

        """
        self.__id = id
        self.__shopping_cart = ShoppingCart()
        self.__role = GuestState()
        self.__logged_in = False

    def transition_to(self, state: State):
        self.__role = state

    def exit(self):
        self.__role.exit()

    def login(self,member_state : MemberState):
        self.__logged_in = True
        self.transition_to(member_state)

    def is_logged_in(self):
        return self.__logged_in
