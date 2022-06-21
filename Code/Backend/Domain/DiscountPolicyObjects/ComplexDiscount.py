from typing import List

from Code.Backend.Domain.DiscountPolicyObjects.Discount import Discount
from Code.Backend.Domain.Product import Product


class ComplexDiscount(Discount):

    def __init__(self, firstDiscount: Discount, secondDiscount: Discount):
        super().__init__(discount=-1, end_date="", discount_on="", Type=-1)
        self.firstDiscount = firstDiscount
        self.secondDiscount = secondDiscount

    def calculate_price(self, quantity_dict, products, dic_to_update):
        pass

