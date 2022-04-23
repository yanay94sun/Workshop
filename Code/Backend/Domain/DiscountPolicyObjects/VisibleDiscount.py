from Code.Backend.Domain.DiscountPolicyObjects.Discount import Discount


class VisibleDiscount(Discount):

    def __init__(self, discount, end_date, rules=[], products_ids=[]):

        super().__init__(discount, end_date, rules, products_ids)

    def calculate_price(self, quantity_dict, products, dic_to_update, invisible_code):
        if all(map(lambda r: r.enforce_rule(products, quantity_dict), self.rules)):
            for p in products:
                if self.products_ids is not []:
                    if p.get_ID() in self.products_ids:
                        dic_to_update[0][p.get_ID()].append(self.my_discount)
                else:
                    dic_to_update[0][p.get_ID()].append(self.my_discount)

