from typing import Dict, List

from Code.Backend.Domain.Product import Product


class Discount:

    def __init__(self, discount, end_date):
        self.rules = []
        self.products_ids = []
        self.my_discount: float = discount
        self.end_date = end_date

    def calculate_price(self, quantity_dict: Dict[str,int], products: List[Product], dic_to_update, invisible_code):
        pass
