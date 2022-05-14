from typing import Dict, List

from Code.Backend.Domain.Product import Product


class Discount:

    def __init__(self, discount, end_date, products_ids, by_category="", by_store=False):
        """
        as default, no rules are made and every product get the discount
        """
        self.discount_id = -1
        self.products_ids = products_ids
        self.my_discount: float = discount
        self.end_date = end_date
        self.by_category = by_category
        self.by_store = by_store
        # Todo add field for category and store

    def calculate_price(self, quantity_dict: Dict[str, int], products: List[Product], dic_to_update):
        pass

    def check_condition(self, quantity_dict, products):
        pass

    def set_id(self, id):
        self.discount_id = id

    def get_id(self):
        return self.discount_id
