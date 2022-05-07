from Code.Backend.Domain.ShoppingCart import ShoppingCart


class State:
    def __init__(self, shopping_cart: ShoppingCart):
        self._shopping_cart = shopping_cart

    def exit(self):
        pass

    def get_shopping_cart(self) -> ShoppingCart:
        return self._shopping_cart

    def is_logged_in(self):
        pass

    def add_product_to_shopping_cart(self, product_info):
        return self._shopping_cart.add_product(product_info)

