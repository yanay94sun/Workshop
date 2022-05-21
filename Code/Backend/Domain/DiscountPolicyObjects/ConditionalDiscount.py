from Code.Backend.Domain.DiscountPolicyObjects.Discount import Discount


class ConditionalDiscount(Discount):
    def __init__(self, discount, end_date, discount_on, Type,
                 dic_of_products_and_quantity, min_price_for_discount):

        super().__init__(discount, end_date, discount_on, Type)
        self.products_to_have_for_discount = dic_of_products_and_quantity
        self.min_price_for_discount = min_price_for_discount

    def calculate_price(self, quantity_dict, products, dic_to_update):
        if self.check_condition(quantity_dict, products):
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
        if self.products_to_have_for_discount:
            for key, value in self.products_to_have_for_discount.items():
                if key not in quantity_dict.keys() or value > quantity_dict[key]:
                    return False
        elif self.min_price_for_discount != 0:
            price = 0
            for p in products:
                price += p.get_price() * quantity_dict[p.get_ID]
            if price < self.min_price_for_discount:
                return False
        return True
