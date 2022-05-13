from typing import List

from Code.Backend.Domain.DiscountPolicyObjects.Discount import Discount
from Code.Backend.Domain.Product import Product


class ComplexDiscount(Discount):

    def __init__(self, firstDiscount: Discount, secondDiscount: Discount):
        super().__init__(discount=0, end_date="", products_ids={})
        self.firstDiscount = firstDiscount
        self.secondDiscount = secondDiscount

    def calculate_price(self, quantity_dict, products, dic_to_update):
        pass

