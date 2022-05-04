from Code.Backend.Domain.StoreOfficials.Permissions import Permissions, Actions
from Code.Backend.Domain.StoreOfficials.StoreOfficial import StoreOfficial


class StoreManager(StoreOfficial):
    def __init__(self, just_appointed: str,  # memder id
                 old_appointee: StoreOfficial):
        super().__init__(just_appointed, old_appointee)
        self.permissions = Permissions({Actions.INVENTORY_ACTION: False,
                                        Actions.CHANGE_MANAGER_PERMISSION: False,
                                        Actions.ADD_STORE_MANAGER: False,
                                        Actions.ADD_STORE_OWNER: False,
                                        Actions.GET_STORE_PURCHASE_HISTORY: True,
                                        Actions.CLOSE_STORE: False,
                                        Actions.GET_STORE_ROLES: False})

    def check_permission(self, action):
        return self.permissions.check_permission(action)

    def set_permission(self, new_permission):
        self.permissions.set_permission(new_permission)
