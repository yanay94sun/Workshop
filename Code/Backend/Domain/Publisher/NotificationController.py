

class NotificationController:
    def __init__(self):
        self.__stores_activity = {}  # store_id, [activities]

    def subscribe(self, username, store_id, activity):