from typing import Dict, List

from Code.Backend.Domain.Product import Product
from Code.Backend.Domain.PurchasePolicyObjects.AndPurchaseRule import AndPurchaseRule
from Code.Backend.Domain.PurchasePolicyObjects.OrPurchaseRule import OrPurchaseRule
from Code.Backend.Domain.PurchasePolicyObjects.PurchaseRule import PurchaseRule
from Code.Backend.Domain.PurchasePolicyObjects.SimplePurchaseRule import SimplePurchaseRule


class PurchasePolicy:
    def __init__(self):
        """
        conditional not implemented
        """
        self.purchase_rules: Dict[int, PurchaseRule] = {}
        self.id_counter = 0

    def can_buy(self, products: List[Product], user_status, quantity_dic):
        for rule in self.purchase_rules.values():
            if not rule.enforce_rule(products, user_status, quantity_dic):
                return False
        return True

    def add_simple_purchase_rule(self, products_to_have_for_purchase,
                                 min_price_to_have_for_purchase, by_category, by_store):
        self.id_counter += 1
        purchase_rule = SimplePurchaseRule(products_to_have_for_purchase, min_price_to_have_for_purchase,
                                           by_category, by_store)
        purchase_rule.set_id(self.id_counter)
        self.purchase_rules[self.id_counter] = purchase_rule
        return purchase_rule

    def add_and_purchase_rule(self, first_rule, second_rule):
        try:
            rule1 = self.purchase_rules.pop(first_rule)
            rule2 = self.purchase_rules.pop(second_rule)
            self.id_counter += 1
            rule = AndPurchaseRule(rule1, rule2)
            rule.set_id(self.id_counter)
            self.purchase_rules[self.id_counter] = rule
            return rule
        except:
            raise ValueError("no discount was found with the given id")

    def add_or_purchase_rule(self, first_rule, second_rule):
        try:
            rule1 = self.purchase_rules.pop(first_rule)
            rule2 = self.purchase_rules.pop(second_rule)
            self.id_counter += 1
            rule = OrPurchaseRule(rule1, rule2)
            rule.set_id(self.id_counter)
            self.purchase_rules[self.id_counter] = rule
            return rule
        except:
            raise ValueError("no discount was found with the given id")
