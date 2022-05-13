from functools import reduce
from typing import Dict, List

from Code.Backend.Domain.DiscountPolicyObjects.ConditionalDiscount import ConditionalDiscount
from Code.Backend.Domain.DiscountPolicyObjects.OrDiscount import OrDiscount
from Code.Backend.Domain.DiscountPolicyObjects.VisibleDiscount import VisibleDiscount
from Code.Backend.Domain.Product import Product


class DiscountPolicy:
    def __init__(self):
        """
        """
        self.__discounts = []
        self.__authorized_for_discount = None  # TODO

    def calculate_basket(self, products: List[Product], user_status, quantity_dic, invisible_codes):
        # TODO need to check if user is authorized.
        products_discounts: Dict[str, List[float]] = {prdct.get_ID(): [] for prdct in
                                                      products}
        for discount in self.__discounts:
            discount.calculate_price(quantity_dic, products, [products_discounts], invisible_codes)
        price = 0
        for p in products:
            # check if there is a discount
            if products_discounts[p.get_ID()]:
                price += (p.get_price() * quantity_dic[p.get_ID()]) \
                         - (max(products_discounts[p.get_ID()])) * p.get_price() * quantity_dic[p.get_ID()]
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

    def add_visible_discount(self, list_of_products_ids, discount_price, end_date):
        if discount_price >= 1:
            raise ValueError("cant get discount over 100%")
        discount = VisibleDiscount(discount_price, end_date, products_ids=list_of_products_ids)
        self.__discounts.append(discount)
        return discount

    def add_conditional_discount(self, list_of_products_ids, discount_price, end_date, dic_of_products_and_quantity,
                                 min_price_for_discount):
        if discount_price >= 1:
            raise ValueError("cant get discount over 100%")
        discount = ConditionalDiscount(discount_price, end_date, list_of_products_ids,
                                       dic_of_products_and_quantity=dic_of_products_and_quantity,
                                       min_price_for_discount=min_price_for_discount)
        self.__discounts.append(discount)
        return discount

    def add_or_discount(self, first_discount, second_discount):
        discount = OrDiscount(first_discount, second_discount)
        self.__discounts.append(discount)
        return discount
