class SupplyService:
    def __init__(self):
        """


        """
        self.inventory = {"1": 200,
                          "2": 300,
                          "3": 400,
                          "4": 500,
                          "5": 600,
                          "6": 250,
                          "7": 340,
                          "8": 450}

    def check_product_in_stock(self, p_id, quantity):
        if p_id in self.inventory.keys() and self.inventory[p_id] >= quantity:
            return True
        return False

    # the function gets dict of {prod_id : quantity}

    def supply(self, supply_info):
        for p_id, quantity in supply_info.get_supply_info.items():
            if not self.check_product_in_stock(id, quantity):
                return False
        for p_id, quantity in supply_info.get_supply_info.items():
            self.inventory[p_id] -= quantity
        return True

    def make_connection(self, market):
        # mock, just for example
        if 1 > 0:
            return self
        else:
            return None