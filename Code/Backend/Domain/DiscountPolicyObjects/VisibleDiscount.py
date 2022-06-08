from Code.Backend.Domain.DiscountPolicyObjects.Discount import Discount


class VisibleDiscount(Discount):

    def __init__(self, discount, end_date, discount_on, Type):

        super().__init__(discount, end_date, discount_on, Type)

    def calculate_price(self, quantity_dict, products, dic_to_update):
        for p in products:
            if self.Type == 1:
                if p.get_ID() == self.discount_on:
                    dic_to_update[0][p.get_ID()].append(self.my_discount)
            elif self.Type == 2:
                if p.get_category() == self.discount_on:
                    dic_to_update[0][p.get_ID()].append(self.my_discount)
            else:
                dic_to_update[0][p.get_ID()].append(self.my_discount)

    def check_condition(self, quantity_dict, products):
        return True
