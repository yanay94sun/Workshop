from Code.Backend.Domain.StoreOfficials.StoreFounder import StoreFounder
from Code.Backend.Domain.StoreOfficials.StoreOfficial import StoreOfficial


class Permissions:
    # def __init__(self, is_owner, appointee_id):
    #     self.__is_owner = is_owner
    #     self.__permissions = {1: True, 2: True, 3: True, 4: True, 5: True, 6: True, 7: True}
    #     self.__appointee_id = appointee_id
    def __init__(self, parent: StoreOfficial):
        if isinstance(parent, StoreFounder):
            self.__permissions = {i: True for i in range(7)}
        else:
            self.__permissions = {i: parent.check_permission(i) for i in range(7)}
        # todo: if more actions added need to increase the range

    def check_permission(self, action_number):
        return self.__permissions[action_number.value]

    def set_permission(self, action_number, new_val):
        if action_number.value in self.__permissions.keys():
            self.__permissions[action_number.value] = new_val
    #
    # def get_appointee_id(self):
    #     return self.__appointee_id
    #
    # def get_is_owner(self):
    #     return self.__is_owner
    #
    # def change_is_owner(self,new_value):
    #     self.__is_owner = new_value
