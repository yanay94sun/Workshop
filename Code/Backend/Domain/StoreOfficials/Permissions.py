from typing import Dict

from Code.Backend.Domain.StoreOfficials.StoreFounder import StoreFounder
from Code.Backend.Domain.StoreOfficials.StoreOfficial import StoreOfficial
from enum import Enum


class Permissions:
    def __init__(self, permission: Dict):
        self.__permissions = permission

    def check_permission(self, action_number):
        return self.__permissions[action_number.value]

    def set_permission(self, new_val):
        self.__permissions = new_val


class Actions(Enum):
    INVENTORY_ACTION = 1
    ADD_STORE_OWNER = 2
    ADD_STORE_MANAGER = 3
    CHANGE_MANAGER_PERMISSION = 4
    CLOSE_STORE = 5
    GET_STORE_ROLES = 6
    GET_STORE_PURCHASE_HISTORY = 7
    DISCOUNT_MANAGEMENT = 8
    PURCHASE_MANAGEMENT = 9
