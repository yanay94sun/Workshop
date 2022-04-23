from Code.Backend.Domain.StoreOfficials.StoreOfficial import StoreOfficial
from Code.Backend.Service.Objects.Permissions import Permission


class StoreManager(StoreOfficial):
    def __init__(self, just_appointed: StoreOfficial,
                 old_appointee: StoreOfficial,
                 permissions: Permission):
        super().__init__(just_appointed, old_appointee)
        self.permissions = permissions
