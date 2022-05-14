from Code.Backend.Domain.DiscountPolicyObjects.Discount import Discount


class ConditionalDiscount(Discount):
    def __init__(self, discount, end_date, products_ids,
                 dic_of_products_and_quantity={}, min_price_for_discount=0):
        super().__init__(discount, end_date, products_ids)
        self.products_to_have_for_discount = dic_of_products_and_quantity
        self.min_price_for_discount = min_price_for_discount

    def calculate_price(self, quantity_dict, products, dic_to_update):
        if self.check_condition(quantity_dict, products):
            for p in products:
                if p.get_ID() in self.products_ids:
                    dic_to_update[0][p.get_ID()].append(self.my_discount)

    def check_condition(self, quantity_dict, products):
        if self.products_to_have_for_discount != {}:
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
