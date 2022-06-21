from typing import Dict, List

from Code.Backend.Domain.Product import Product


class Discount:

    def __init__(self, discount, end_date, discount_on, Type):
        """
        as default, no rules are made and every product get the discount
        """
        self.discount_id = -1
        self.discount_on = discount_on
        self.my_discount: float = discount
        self.end_date = end_date
        self.Type = Type   #  1: = by product, 2: by category, 3: by store

    def calculate_price(self, quantity_dict: Dict[str, int], products: List[Product], dic_to_update):
        pass

    def check_condition(self, quantity_dict, products):
        pass

    def set_id(self, id):
        self.discount_id = id

    def get_id(self):
        return self.discount_id
