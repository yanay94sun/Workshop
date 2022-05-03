from Code.Backend.Domain.StoreOfficials.StoreOfficial import StoreOfficial


class StoreFounder(StoreOfficial):
    def __init__(self, just_appointed: str,  # member id
                 old_appointee: StoreOfficial):
        super().__init__(just_appointed, old_appointee)

    def check_permission(self, action):
        return True

    def set_permission(self, action_number, new_val):
        raise Exception("can't change founder's permissions")
