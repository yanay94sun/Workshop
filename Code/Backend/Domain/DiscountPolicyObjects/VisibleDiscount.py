from Code.Backend.Domain.DiscountPolicyObjects.Discount import Discount


class VisibleDiscount(Discount):

    def __init__(self, discount, end_date, products_ids, by_category, by_store):

        super().__init__(discount, end_date, products_ids, by_category, by_store)

    def calculate_price(self, quantity_dict, products, dic_to_update):
        for p in products:
            if self.products_ids:
                if p.get_ID() in self.products_ids:
                    dic_to_update[0][p.get_ID()].append(self.my_discount)

            elif self.by_category != "":
                if p.get_category() == self.by_category:
                    dic_to_update[0][p.get_ID()].append(self.my_discount)

            elif self.by_store:
                dic_to_update[0][p.get_ID()].append(self.my_discount)

    def check_condition(self, quantity_dict, products):
        return True
