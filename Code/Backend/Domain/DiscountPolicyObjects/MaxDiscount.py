from typing import Dict, List

from Code.Backend.Domain.DiscountPolicyObjects.ComplexDiscount import ComplexDiscount


class MaxDiscount(ComplexDiscount):
    def __init__(self, firstDiscount, secondDiscount):
        super().__init__(firstDiscount, secondDiscount)

    def calculate_price(self, quantity_dict, products, dic_to_update):
        # check if both discount met their condition, if they do add,
        tmp_dic_to_update: Dict[str, List[float]] = {prdct.get_ID(): [] for prdct in
                                                     products}
        if self.check_condition(quantity_dict, products):
            self.firstDiscount.calculate_price(quantity_dict, products, [tmp_dic_to_update])
            self.secondDiscount.calculate_price(quantity_dict, products, [tmp_dic_to_update])

        # if only one discount met her condition, calculate its price
        elif self.firstDiscount.check_condition(quantity_dict, products):
            self.firstDiscount.calculate_price(quantity_dict, products, [tmp_dic_to_update])

        elif self.secondDiscount.check_condition(quantity_dict, products):
            self.secondDiscount.calculate_price(quantity_dict, products, [tmp_dic_to_update])

        # if they both didn't meet their condition, do nothing
        for key in tmp_dic_to_update.keys():
            dic_to_update[0][key].append(max(tmp_dic_to_update[key]))

    def check_condition(self, quantity_dict, products):
        return self.firstDiscount.check_condition(quantity_dict, products) and \
               self.secondDiscount.check_condition(quantity_dict, products)
