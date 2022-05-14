from typing import List, Dict

from Code.Backend.Domain.Product import Product


class PurchaseRule:
    def __init__(self, products_to_have_for_purchase: Dict[str, int],
                 min_price_to_have_for_purchase: int, by_category: str,
                 by_store):
        """
        add to products_to_have_for_purchase if the condition is "at least x of product y"
        add to min_price_to_have_for_purchase if the condition is "at least x of total cart price"
        add to by_category if the condition is "the cart should have at least one product of category x"
        by store i don't know...
        """
        self.products_to_have_for_purchase = products_to_have_for_purchase
        self.min_price_to_have_for_purchase = min_price_to_have_for_purchase
        self.by_category = by_category
        self.by_store = by_store
        self.purchase_rule_id = -1

    def enforce_rule(self, products: List[Product], user_status, quantity_dic):
        pass

    def set_id(self, id):
        self.purchase_rule_id = id

    def get_id(self):
        return self.purchase_rule_id
