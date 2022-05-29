# from typing import List, Dict
from typing import Dict

from Code.Backend.Domain.Product import Product
from collections.abc import Sequence
from pydantic import BaseModel
from pydantic.class_validators import Optional


class PackageInfo(BaseModel):
    # def __init__(self, costumer_name, costumer_last_name, costumer_address,
    #              store_id, products_ids_and_quantity: Dict[str, int]):
    #     self.costumer_name = costumer_name
    #     self.costume_last_name = costumer_last_name
    #     self.costumer_address = costumer_address
    #     self.store_id = store_id
    #     self.products_ids_and_quantity = products_ids_and_quantity
    costumer_name: str
    costumer_last_name: str
    costumer_address: str
    store_id: str
    products_ids_and_quantity: Dict[str, int]
