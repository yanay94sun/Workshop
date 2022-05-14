from Code.Backend.Domain.PurchasePolicyObjects.PurchaseRule import PurchaseRule


class ComplexPurchaseRule(PurchaseRule):
    def __init__(self, first_rule: PurchaseRule, second_rule: PurchaseRule):
        super().__init__(products_to_have_for_purchase={}, min_price_to_have_for_purchase=0, by_category="", by_store=-1)
        self.first_rule = first_rule
        self.second_rule = second_rule
