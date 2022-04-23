from typing import List, Dict

from Code.Backend.Domain.Product import Product
from collections.abc import Sequence


class PackageInfo:
    def __init__(self, costumer_name, costumer_last_name, costumer_address,
                 store_id, products_ids_and_quantity: Dict[str, int]):
        self.costumer_name = costumer_name
        self.costume_last_name = costumer_last_name
        self.costumer_address = costumer_address
        self.store_id = store_id
        self.products_ids_and_quantity = products_ids_and_quantity

    def get_costumer_name(self):
        return self.costumer_name

    def get_costumer_last_name(self):
        return self.get_costumer_last_name()

    def get_costumer_address(self):
        return self.costumer_address

    def get_store_id(self):
        return self.store_id

    def get_products_ids_and_quantity(self):
        return self.products_ids_and_quantity
