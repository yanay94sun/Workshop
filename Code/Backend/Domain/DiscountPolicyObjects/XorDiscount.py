from Code.Backend.Domain.DiscountPolicyObjects.ComplexDiscount import ComplexDiscount


class XorDiscount(ComplexDiscount):
    def __init__(self, firstDiscount, secondDiscount):
        super().__init__(firstDiscount, secondDiscount)

    def calculate_price(self, quantity_dict, products, dic_to_update):
        if self.__check_first_condition(quantity_dict, products):
            self.firstDiscount.calculate_price(quantity_dict, products, dic_to_update)
        elif self.__check_second_condition(quantity_dict, products):
            self.secondDiscount.calculate_price(quantity_dict, products, dic_to_update)

    def check_condition(self, quantity_dict, products):
        return self.firstDiscount.check_condition(quantity_dict, products) or \
               self.secondDiscount.check_condition(quantity_dict, products)

    def __check_first_condition(self, quantity_dict, products):
        return self.firstDiscount.check_condition(quantity_dict, products)

    def __check_second_condition(self, quantity_dict, products):
        return self.secondDiscount.check_condition(quantity_dict, products)
