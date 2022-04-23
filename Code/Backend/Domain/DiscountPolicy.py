from functools import reduce
from typing import Dict, List

from Code.Backend.Domain.DiscountPolicyObjects.VisibleDiscount import VisibleDiscount
from Code.Backend.Domain.Product import Product


class DiscountPolicy:
    def __init__(self):
        """
        """
        self.__discounts = []
        self.__authorized_for_discount = None  # TODO
        self.__doubled_discounts = True

    def add_discount(self, list_of_products, discount_type, rule=None):
        pass

    def change_doubled_discounts(self, new_val):
        self.__doubled_discounts = new_val

    def calculate_basket(self, products: List[Product], user_status, quantity_dic, invisible_codes):
        # need to check if user is authorized.
        products_discounts: Dict[str, List[float]] = {prdct.get_ID(): [] for prdct in
                                                      products}
        for discount in self.__discounts:
            discount.calculate_price(quantity_dic, products, [products_discounts], invisible_codes)
        price = 0
        for p in products:
            # check if there is a discount
            if products_discounts[p.get_ID()] is not []:
                if self.__doubled_discounts:
                    price += (p.get_price() * quantity_dic[p.get_ID()]) \
                             - (reduce((lambda x, y: x + y), products_discounts[p.get_ID()])) * p.get_price()
                else:
                    price += (p.get_price() * quantity_dic[p.get_ID()]) \
                             - (max(products_discounts[p.get_ID()])) * p.get_price()
            # if not discount
            else:
                price += p.get_price() * quantity_dic[p.get_ID()]

        return price

    def get_visible_discounts(self):
        lst = []
        for discount in self.__discounts:
            if isinstance(discount, VisibleDiscount):
                lst.append(discount)
        return lst
