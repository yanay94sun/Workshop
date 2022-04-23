from Code.Backend.Service.Objects.Permissions import Permission


def check_circular_appoints(just_appointed):
    cur = just_appointed
    while cur:
        if cur == just_appointed:
            return False
    return True


class StoreOfficial:
    def __init__(self, just_appointed: StoreOfficial,
                 old_appointee: StoreOfficial,
                 permission: Permission):
        assert check_circular_appoints(just_appointed)
        self.appointee = old_appointee
        self.appointed = just_appointed
