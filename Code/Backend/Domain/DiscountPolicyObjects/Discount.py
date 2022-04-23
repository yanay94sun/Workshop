from typing import Dict, List

from Code.Backend.Domain.Product import Product


class Discount:

    def __init__(self, discount, end_date, rules, products_ids):
        """
        as default, no rules are made and every product get the discount
        """
        self.rules = rules
        self.products_ids = products_ids
        self.my_discount: float = discount
        self.end_date = end_date

    def calculate_price(self, quantity_dict: Dict[str, int], products: List[Product], dic_to_update, invisible_code):
        pass
