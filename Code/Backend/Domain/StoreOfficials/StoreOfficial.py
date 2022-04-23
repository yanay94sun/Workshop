from Code.Backend.Domain.VisitorStates.MemberState import MemberState
from Code.Backend.Service.Objects.Permissions import Permission


# def check_circular_appoints(just_appointed, old_appointee):
#     cur = old_appointee
#     while cur:
#         if cur.appointed == just_appointed:
#             return False
#         cur = cur.appointee
#     return True


class StoreOfficial:
    def __init__(self, just_appointed: str,  # member id
                 old_appointee):  # StoreOfficial
        # assert check_circular_appoints(just_appointed, old_appointee)
        self.appointee = old_appointee
        self.appointed = just_appointed

    def check_permission(self, action):
        pass

    def set_permission(self, action_number, new_val):
        pass
