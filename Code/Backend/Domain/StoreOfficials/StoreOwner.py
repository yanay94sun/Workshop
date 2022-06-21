from Code.Backend.Domain.StoreOfficials.Permissions import Permissions, Actions
from Code.Backend.Domain.StoreOfficials.StoreOfficial import StoreOfficial


class StoreOwner(StoreOfficial):
    def __init__(self, just_appointed: str,  # member id
                 old_appointee: StoreOfficial,):
        super().__init__(just_appointed, old_appointee)
        self.permissions = Permissions({Actions.INVENTORY_ACTION.value: True,
                                        Actions.CHANGE_MANAGER_PERMISSION.value: True,
                                        Actions.ADD_STORE_MANAGER.value: True,
                                        Actions.ADD_STORE_OWNER.value: True,
                                        Actions.GET_STORE_PURCHASE_HISTORY.value: True,
                                        Actions.CLOSE_STORE.value: False,
                                        Actions.GET_STORE_ROLES.value: True,
                                        Actions.DISCOUNT_MANAGEMENT: True,
                                        Actions.PURCHASE_MANAGEMENT: True})

    def check_permission(self, action):
        return self.permissions.check_permission(action)

    def set_permission(self, new_permission):
        self.permissions = new_permission
