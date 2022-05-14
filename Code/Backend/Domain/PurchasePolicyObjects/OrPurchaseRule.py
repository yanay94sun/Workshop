from Code.Backend.Domain.PurchasePolicyObjects.ComplexPurchaseRule import ComplexPurchaseRule


class OrPurchaseRule(ComplexPurchaseRule):
    def __init__(self, first_rule, second_rule):
        super().__init__(first_rule, second_rule)

    def enforce_rule(self, products, user_status, quantity_dic):
        return self.first_rule.enforce_rule(products, user_status, quantity_dic) or \
               self.second_rule.enforce_rule(products, user_status, quantity_dic)
