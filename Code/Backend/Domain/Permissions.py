from Code.Backend.Domain.Actions import Actions


class Permissions:
    def __init__(self, is_owner):
        self.is_owner = is_owner
        self.__permissions = {1: True, 2: True, 3: True, 4: True, 5: True, 6: True, 7: True}

    def check_permission(self, action_number):
        if self.is_owner:
            return True
        return self.permissions[action_number.value]

    def set_permission(self, action_number, new_val):
        if action_number in self.__permissions.keys():
            self.__permissions[action_number] = new_val
