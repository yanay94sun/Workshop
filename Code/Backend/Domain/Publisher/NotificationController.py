from fromGit.Workshop.Code.Backend.Domain.Controllers.UserController import UserController


class NotificationController:
    def __init__(self, user_controller: UserController):
        self.__uc = user_controller
        self.__stores_activity = {}  # store_id, [activities]

    def subscribe(self, username: str, store_id: str, activity: int):
        self.__stores_activity[store_id][activity].append(username)

    def notify_all(self, store_id: str, activity: int, msg: str):
        for username in self.__stores_activity[store_id][activity]:
            if self.__uc.is_logged_in()