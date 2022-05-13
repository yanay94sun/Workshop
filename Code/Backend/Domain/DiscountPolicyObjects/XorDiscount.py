from typing import List

from Code.Backend.Domain.DiscountPolicyObjects.ComplexDiscount import ComplexDiscount
from Code.Backend.Domain.Product import Product


class XorDiscount(ComplexDiscount):
    def __init__(self,firstDiscount,secondDiscount):
        super().__init__(firstDiscount,secondDiscount)

    def calculate_price(self, quantity_dict, products, dic_to_update):
        pass
