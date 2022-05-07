
class StoreOfficial:
    def __init__(self, just_appointed: str,  # member id
                 old_appointee):  # StoreOfficial
        self.appointee = old_appointee
        self.appointed = just_appointed

    def check_permission(self, action):
        pass

    def set_permission(self, new_permission):
        pass
