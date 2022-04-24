from Code.Backend.Domain.Permissions import Permissions
from Code.Backend.Domain.StoreOfficials.StoreOfficial import StoreOfficial


class StoreManager(StoreOfficial):
    def __init__(self, just_appointed: str,  # memder id
                 old_appointee: StoreOfficial,
                 permissions: Permissions):
        super().__init__(just_appointed, old_appointee)
        self.permissions = permissions

    def check_permission(self, action):
        return self.permissions.check_permission(action)

    def set_permission(self, action_number, new_val):
        self.permissions.set_permission(action_number, new_val)
