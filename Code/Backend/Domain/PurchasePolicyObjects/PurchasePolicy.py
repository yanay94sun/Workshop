from typing import Dict, List

from Code.Backend.Domain.Product import Product
from Code.Backend.Domain.PurchasePolicyObjects.AndPurchaseRule import AndPurchaseRule
from Code.Backend.Domain.PurchasePolicyObjects.OrPurchaseRule import OrPurchaseRule
from Code.Backend.Domain.PurchasePolicyObjects.PurchaseRule import PurchaseRule
from Code.Backend.Domain.PurchasePolicyObjects.SimplePurchaseRule import SimplePurchaseRule
from Code.DAL.Objects.store import PurchaseRule as PurchaseRuleDB


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

    def create_purchase_policy_from_db(self, purchase_rules, complex_purchase_rules, id_counter):
        persist_rules = {x.id: self.__create_simple_rule_from_db(x) for x in purchase_rules}
        persist_complex_discounts = self.__create_complex_rule_from_db(complex_purchase_rules, persist_rules)
        self.purchase_rules = persist_rules.update(persist_complex_discounts)
        self.id_counter = id_counter

    def __create_simple_rule_from_db(self, ruleDB: PurchaseRuleDB):
        prod_for_purchase = {}
        if ruleDB.product_id != '':
            prod_for_purchase = {ruleDB.product_id: ruleDB.quantity}
        rule = SimplePurchaseRule(prod_for_purchase, ruleDB.min_price_to_have, ruleDB.category)
        rule.set_id(ruleDB.id)
        return rule

    def __create_complex_rule_from_db(self, complex_purchase_rules, persist_rules):
        res = {}
        for ruleDB in complex_purchase_rules:
            self.__complex_rec(ruleDB.id, complex_purchase_rules, persist_rules, res)
        return res

    def __complex_rec(self, rule_id, complex_purchase_rules, persist_rules, res):
        curRuleDB = next(filter(lambda x: x.id == rule_id, complex_purchase_rules))
        # exit term
        if not curRuleDB or (curRuleDB and curRuleDB.id in res.keys()):
            return
        # check if not complex rule is son
        if curRuleDB.first_discount in persist_rules.keys():
            first_discount = persist_rules[curRuleDB.first_discount]
        else:
            # check if already made the complex discount
            if curRuleDB.first_discount in res.keys():
                first_discount = res[curRuleDB.first_discount]
            else:
                first_discount = self.__complex_rec(curRuleDB.first_discount, complex_purchase_rules, persist_rules,
                                                    res)
        # check if not complex discount is son
        if curRuleDB.second_discount in persist_rules.keys():
            second_discount = persist_rules[curRuleDB.second_discount]
        else:
            # check if already made the complex discount
            if curRuleDB.second_discount in res.keys():
                second_discount = res[curRuleDB.second_discount]
            else:
                second_discount = self.__complex_rec(curRuleDB.second_discount, complex_purchase_rules, persist_rules,
                                                     res)

        if curRuleDB.type_ == 0:  # or
            rule = OrPurchaseRule(first_discount, second_discount)
        else:  # 2 and
            rule = AndPurchaseRule(first_discount, second_discount)
        rule.set_id(curRuleDB.id)
        res[rule.get_id()] = rule
        return rule
