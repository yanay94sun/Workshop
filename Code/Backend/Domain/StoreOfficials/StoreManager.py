from Code.Backend.Domain.StoreOfficials.Permissions import Permissions, Actions
from Code.Backend.Domain.StoreOfficials.StoreOfficial import StoreOfficial


class StoreManager(StoreOfficial):
    def __init__(self, just_appointed: str,  # memder id
                 old_appointee: StoreOfficial):
        super().__init__(just_appointed, old_appointee)
        self.permissions = Permissions({Actions.INVENTORY_ACTION.value: False,
                                        Actions.CHANGE_MANAGER_PERMISSION.value: False,
                                        Actions.ADD_STORE_MANAGER.value: False,
                                        Actions.ADD_STORE_OWNER.value: False,
                                        Actions.GET_STORE_PURCHASE_HISTORY.value: True,
                                        Actions.CLOSE_STORE.value: False,
                                        Actions.GET_STORE_ROLES.value: False,
                                        Actions.PURCHASE_MANAGEMENT.value: False,
                                        Actions.DISCOUNT_MANAGEMENT.value: False})

    def check_permission(self, action):
        return self.permissions.check_permission(action)

    def set_permission(self, new_permission):
        self.permissions.set_permission(new_permission)
