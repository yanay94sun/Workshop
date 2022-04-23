from typing import List

from Code.Backend.Domain.Product import Product
from Code.Backend.Domain.ShoppingBasket import ShoppingBasket


class Rule:

    def enforce_rule(self, products: List[Product], quantity_dict):
        raise NotImplemented()
