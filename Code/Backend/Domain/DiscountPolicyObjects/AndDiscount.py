from Code.Backend.Domain.DiscountPolicyObjects.ComplexDiscount import ComplexDiscount


class AndDiscount(ComplexDiscount):
    def __init__(self,firstDiscount,secondDiscount):
        super().__init__(firstDiscount,secondDiscount)

    def calculate_price(self, quantity_dict, products, dic_to_update):
        if self.check_condition(quantity_dict, products):
            self.firstDiscount.calculate_price(quantity_dict, products, dic_to_update)
            self.secondDiscount.calculate_price(quantity_dict, products, dic_to_update)

    def check_condition(self, quantity_dict, products):
        return self.firstDiscount.check_condition(quantity_dict, products) and \
               self.secondDiscount.check_condition(quantity_dict, products)

