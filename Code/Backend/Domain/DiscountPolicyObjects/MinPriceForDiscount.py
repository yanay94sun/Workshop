from Code.Backend.Domain.DiscountPolicyObjects.Rule import Rule
from Code.Backend.Domain.ShoppingBasket import ShoppingBasket


class MinPriceForDiscount(Rule):

    def __init__(self, price):
        self.price = price

    def enforce_rule(self, products, quantity_dict):
        basket_price = 0
        for p in products:
            basket_price += p.get_price() * quantity_dict[products]
        if basket_price < self.price:
            return False
        return True

