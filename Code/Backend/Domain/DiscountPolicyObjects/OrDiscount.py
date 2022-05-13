from typing import List

from Code.Backend.Domain.DiscountPolicyObjects.ComplexDiscount import ComplexDiscount
from Code.Backend.Domain.Product import Product


class OrDiscount(ComplexDiscount):
    def __init__(self, firstDiscount, secondDiscount):
        super().__init__(firstDiscount, secondDiscount)

    def calculate_price(self, quantity_dict, products, dic_to_update):
        had_discount = self.firstDiscount.calculate_price(quantity_dict, products, dic_to_update) or \
                       self.secondDiscount.calculate_price(quantity_dict, products, dic_to_update)
        return had_discount
