from typing import List

from Code.Backend.Domain.Product import Product
from collections.abc import Sequence

class SupplyInfo:
    def __init__(self, costumer,products_ids_and_quantity: dict[str, int]):
        self.products_ids_and_quantity = products_ids_and_quantity
        self.costumer = costumer

    def get_supply_info(self):
        return self.products_ids_and_quantity
