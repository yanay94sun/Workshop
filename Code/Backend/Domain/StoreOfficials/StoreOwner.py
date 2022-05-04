from Code.Backend.Domain.Permissions import Permissions
from Code.Backend.Domain.StoreOfficials.StoreOfficial import StoreOfficial
from Code.Backend.Domain.VisitorStates.MemberState import MemberState


class StoreOwner(StoreOfficial):
    def __init__(self, just_appointed: str,  # member id
                 old_appointee: StoreOfficial,
                 permissions: Permissions):
        super().__init__(just_appointed, old_appointee)
        self.permissions = permissions

    def check_permission(self, action):
        return self.permissions.check_permission(action)

    def set_permission(self, action_number, new_val):
        raise Exception("can't change owner's permissions")
