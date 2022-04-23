from Code.Backend.Domain.DiscountPolicyObjects.Discount import Discount
from Code.Backend.Domain.Product import Product
from Code.Backend.Domain.ShoppingBasket import ShoppingBasket


class ConditionalDiscount(Discount):
    def __init__(self, discount, end_date, dic_of_products_and_quantity, rules=[], products_ids=[]):
        super().__init__(discount, end_date, rules, products_ids)
        self.products_to_have_for_discount = dic_of_products_and_quantity

    def calculate_price(self, quantity_dict, products, dic_to_update, invisible_code):
        if all(map(lambda r: r.enforse_rule(products, quantity_dict), self.rules)):
            if self.__check_condition(quantity_dict):
                for p in products:
                    if p.get_ID() in self.products_ids:
                        dic_to_update[0][p.get_ID()].append(self.my_discount)

    def __check_condition(self, quantity_dict):
        for key, value in self.products_to_have_for_discount.items():
            if key not in quantity_dict.keys() or value > quantity_dict[key]:
                return False
        return True
