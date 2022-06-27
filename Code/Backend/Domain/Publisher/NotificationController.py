from enum import Enum
from typing import Dict, List

from fastapi import WebSocket

from Code.Backend.Domain.Controllers.UserController import UserController
from Code.Backend.Domain.VisitorStates.MemberState import MemberState

import Code.Backend.Server_FastAPI.messages_sender as server

import asyncio


class Activities(Enum):
    PURCHASE_IN_STORE = 0
    STORE_CLOSED = 1
    STORE_REOPENED = 2
    OFFICIAL_REMOVED = 3



class NotificationController:
    def __init__(self, user_controller: UserController):
        self.__uc = user_controller
        self.__stores_activity: Dict[str, List[List[str]]] = {}  # store_id, list<list<str usernames>>
        self.__phone_book: Dict[str, WebSocket] = {}  # uid, websocket

        self.__event_loop = asyncio.BaseEventLoop()
        self.__event_loop.run_forever()

    def subscribe(self, username: str, store_id: str, activity: Activities):
        self.__stores_activity[store_id][activity.value].append(username)

    def unsubscribe(self, username: str, store_id: str, activity: Activities):
        self.__stores_activity[store_id][activity.value].remove(username)

    def register_store(self, sid, owner_username):
        if sid in self.__stores_activity:
            raise Exception("store already registered in the notifications service")

        self.__stores_activity[sid] = [[owner_username] for _ in Activities]

    def notify_all(self, store_id: str, activity: Activities, msg: str):
        print("in notify_all")
        for username in self.__stores_activity[store_id][activity.value]:
            print(f"sending to {username}")
            self.notify_single(username, msg)


    async def notify_single_task(self, to_username, content):
        accepted_msg = False
        print("in notify_single")
        if self.__uc.is_online(to_username):
            print("notify single 1")
            uid = self.__uc.get_username_uid(to_username)
            print("notify single 2")
            accepted_msg = await server.send_ws_message(content, self.__phone_book[uid])
        if not accepted_msg:
            print("notify single 3")
            res = self.__uc.add_message_to_member(to_username, content)
            if res.error_occurred():
                return res

    def notify_single(self, to_username, content):
        task = self.__event_loop.create_task(self.notify_single_task(to_username, content))
        self.__event_loop.run_until_complete(task)


    def register_connection(self, uid, ws: WebSocket):
        print("notify single 4")
        self.__phone_book[uid] = ws
