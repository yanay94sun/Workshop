from typing import List

from Code.Backend.Domain.DiscountPolicyObjects.Rule import Rule
from Code.Backend.Domain.Product import Product


class OrRule(Rule):
    def __init__(self):
        super().__init__()

    def enforce_rule(self, products: List[Product], quantity_dict):
        pass
