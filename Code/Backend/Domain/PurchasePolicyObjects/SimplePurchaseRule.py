from Code.Backend.Domain.PurchasePolicyObjects.PurchaseRule import PurchaseRule


class SimplePurchaseRule(PurchaseRule):
    def __init__(self, products_to_have_for_purchase, min_price_to_have_for_purchase, by_category, by_store):
        super().__init__(products_to_have_for_purchase, min_price_to_have_for_purchase, by_category, by_store)

    def enforce_rule(self, products, user_status, quantity_dic):
        if self.products_to_have_for_purchase:
            for key, value in self.products_to_have_for_purchase.items():
                if key not in quantity_dic.keys() or value > quantity_dic[key]:
                    return False

        elif self.min_price_to_have_for_purchase != 0:
            price = 0
            for p in products:
                tmpId = p.get_ID()
                price += p.get_price() * quantity_dic[tmpId]
            if price < self.min_price_to_have_for_purchase:
                return False

        elif self.by_category != "":
            for p in products:
                if p.get_category() == self.by_category:
                    return True
            return False
        return True



