from Code.Backend.Domain.DiscountPolicyObjects.Discount import Discount


class InvisibleDiscount(Discount):
    # not implemented

    def __init__(self, discount, end_date, invisible_code, rules=[], products_ids=[]):
        super().__init__(discount, end_date, rules, products_ids)
        self.invisible_code = invisible_code

    def calculate_price(self, quantity_dict, products, dic_to_update, invisible_code):
        if invisible_code == self.invisible_code:
            if all(map(lambda r: r.enforse_rule(products, quantity_dict), self.rules)):
                for p in products:
                    dic_to_update[0][p.get_ID()].append(self.my_discount)
