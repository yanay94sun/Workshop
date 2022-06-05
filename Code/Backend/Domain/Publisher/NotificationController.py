from enum import Enum
from typing import Dict, List

from Code.Backend.Domain.Controllers.UserController import UserController
from Code.Backend.Domain.VisitorStates.MemberState import MemberState


class Activities(Enum):
    PURCHASE_IN_STORE = 0
    OFFICIAL_ADDED = 1
    OFFICIAL_REMOVED = 2



class NotificationController:
    def __init__(self, user_controller: UserController):
        self.__uc = user_controller
        self.__stores_activity: Dict[str, List[List[str]]] = {}  # store_id, list<list<str usernames>>

    def subscribe(self, username: str, store_id: str, activity: int):
        self.__stores_activity[store_id][activity].append(username)

    def unsubscribe(self, username: str, store_id: str, activity: int):
        self.__stores_activity[store_id][activity].remove(username)

    def register_store(self, sid):
        if sid in self.__stores_activity:
            raise Exception("store already registered in the notifications service")

        self.__stores_activity[sid] = [[] for _ in Activities]

    def notify_all(self, store_id: str, activity: int, msg: str):
        for username in self.__stores_activity[store_id][activity]:
            if self.__uc.is_online(username):
                pass  # todo: server.push_notification
            else:
                res = self.__uc.add_message_to_member(username, msg)
                if res.error_occurred():
                    return res