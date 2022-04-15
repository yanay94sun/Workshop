from Code.Backend.Domain.ShoppingCart import ShoppingCart
from Code.Backend.Domain.State import State


class Visitor:
    def __init__(self, id: str):
        """

        """
        self.id = id
        self.shopping_cart = ShoppingCart()
        self._state = None

    def transition_to(self, state: State):
        self._state = state
        self._state.visitor = self




