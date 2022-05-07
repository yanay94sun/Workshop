from Code.Backend.Domain.StoreOfficials.StoreOfficial import StoreOfficial


class StoreFounder(StoreOfficial):
    def __init__(self, just_appointed: str):  # member id
        super().__init__(just_appointed, None)
        self.appointed = just_appointed

    def check_permission(self, action):
        return True

    def set_permission(self, new_permission):
        raise Exception("can't change founder's permissions")
