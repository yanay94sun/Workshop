from typing import List

from Code.Backend.Domain.Product import Product


class Rule:

    def __init__(self):
        pass

    def enforce_rule(self, products: List[Product], quantity_dict):
        raise NotImplemented()
