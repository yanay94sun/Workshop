from Code.Backend.Domain.ShoppingCart import ShoppingCart
from Code.Backend.Domain.State import State


class GuestState(State):
    """
    brand new state for brand new user
    """
    def __init__(self):
        State.__init__(self, ShoppingCart())

    def is_logged_in(self):
        return False

    def exit(self):
        self._shopping_cart = ShoppingCart()



