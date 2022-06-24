from functools import reduce
from typing import Dict, List

from Code.Backend.Domain.DiscountPolicyObjects.AndDiscount import AndDiscount
from Code.Backend.Domain.DiscountPolicyObjects.ConditionalDiscount import ConditionalDiscount
from Code.Backend.Domain.DiscountPolicyObjects.MaxDiscount import MaxDiscount
from Code.Backend.Domain.DiscountPolicyObjects.OrDiscount import OrDiscount
from Code.Backend.Domain.DiscountPolicyObjects.SumDiscount import SumDiscount
from Code.Backend.Domain.DiscountPolicyObjects.VisibleDiscount import VisibleDiscount
from Code.Backend.Domain.DiscountPolicyObjects.XorDiscount import XorDiscount
from Code.Backend.Domain.Product import Product


class DiscountPolicy:
    def __init__(self):
        """
        """
        self.__discounts = {}
        self.__authorized_for_discount = None  # TODO
        self.id_counter = 0

    def calculate_basket(self, products: List[Product], user_status, quantity_dic):
        # TODO need to check if user is authorized.
        products_discounts: Dict[str, List[float]] = {prdct.get_ID(): [] for prdct in
                                                      products}
        for discount in self.__discounts.values():
            discount.calculate_price(quantity_dic, products, [products_discounts])
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
        for discount in self.__discounts.values():
            if isinstance(discount, VisibleDiscount):
                lst.append(discount)
        return lst

    def get_conditional_discounts(self):
        lst = []
        for discount in self.__discounts.values():
            if isinstance(discount, ConditionalDiscount):
                lst.append(discount)
        return lst

    def get_combined_discounts(self):
        lst = []
        for discount in self.__discounts.values():
            if not isinstance(discount, ConditionalDiscount) and not isinstance(discount, VisibleDiscount):
                lst.append(discount)
        return lst

    def add_visible_discount(self, discount_price, end_date, discount_on, Type):
        if discount_price >= 1:
            raise ValueError("cant get discount over 100%")
        if discount_price <= 0:
            raise ValueError("discount cant be 0 or negative")
        self.id_counter += 1
        discount = VisibleDiscount(discount_price, end_date, discount_on, Type)
        discount.set_id(self.id_counter)
        self.__discounts[self.id_counter] = discount
        return discount

    def add_conditional_discount(self, discount_price, end_date, discount_on,
                                 Type, dic_of_products_and_quantity,
                                 min_price_for_discount):
        if discount_price >= 1:
            raise ValueError("cant get discount over 100%")
        if discount_price <= 0:
            raise ValueError("discount cant be 0 or negative")
        self.id_counter += 1
        discount = ConditionalDiscount(discount_price, end_date, discount_on,
                                       Type,
                                       dic_of_products_and_quantity,
                                       min_price_for_discount)
        discount.set_id(self.id_counter)
        self.__discounts[self.id_counter] = discount
        return discount

    def add_or_discount(self, first_discount, second_discount):
        try:
            discount1 = self.__discounts.pop(first_discount)
            discount2 = self.__discounts.pop(second_discount)
            self.id_counter += 1
            discount = OrDiscount(discount1, discount2)
            discount.set_id(self.id_counter)
            self.__discounts[self.id_counter] = discount
            return discount
        except:
            raise ValueError("no discount was found with the given id")

    def add_and_discount(self, first_discount, second_discount):
        try:
            discount1 = self.__discounts.pop(first_discount)
            discount2 = self.__discounts.pop(second_discount)
            self.id_counter += 1
            discount = AndDiscount(discount1, discount2)
            discount.set_id(self.id_counter)
            self.__discounts[self.id_counter] = discount
            return discount
        except:
            raise ValueError("no discount was found with the given id")

    def add_xor_discount(self, first_discount, second_discount):
        try:
            discount1 = self.__discounts.pop(first_discount)
            discount2 = self.__discounts.pop(second_discount)
            self.id_counter += 1
            discount = XorDiscount(discount1, discount2)
            discount.set_id(self.id_counter)
            self.__discounts[self.id_counter] = discount
            return discount
        except:
            raise ValueError("no discount was found with the given id")

    def add_sum_discount(self, first_discount, second_discount):
        try:
            discount1 = self.__discounts.pop(first_discount)
            discount2 = self.__discounts.pop(second_discount)
            self.id_counter += 1
            discount = SumDiscount(discount1, discount2)
            discount.set_id(self.id_counter)
            self.__discounts[self.id_counter] = discount
            return discount
        except:
            raise ValueError("no discount was found with the given id")

    def add_max_discount(self, first_discount, second_discount):
        try:
            discount1 = self.__discounts.pop(first_discount)
            discount2 = self.__discounts.pop(second_discount)
            self.id_counter += 1
            discount = MaxDiscount(discount1, discount2)
            discount.set_id(self.id_counter)
            self.__discounts[self.id_counter] = discount
            return discount
        except:
            raise ValueError("no discount was found with the given id")
