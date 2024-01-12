from enum import Enum
from uuid import uuid4


class EventName(Enum):
    PLAYER_NAME_CHANGE = 1
    PLAYER_STATUS_CHANGE = 2
    PLAYER_SCORE_CHANGE = 3
    PLAYER_ADDED = 4
    NEW_ROUND = 5


class EventHandler:

    def __init__(self):
        self.subscribers_players = {}
        self.subscribers_global = []

    def subscribe_player(self, event_name: EventName, player_id, action):
        key = uuid4().hex
        self.subscribers_players.update({key: (event_name, player_id, action)})
        return key

    def unsubscribe_player(self, key):
        self.subscribers_players.pop(key)

    def subscribe_global(self, event_name: EventName, action):
        self.subscribers_global.append((event_name, action))

    def fire_player(self, event_name: EventName, player_id):
        for subscriber in self.subscribers_players.values():
            if subscriber[0] == event_name and subscriber[1] == player_id:
                subscriber[2]()
        self.fire_global(event_name)

    def fire_global(self, event_name: EventName):
        for subscriber in self.subscribers_global:
            if subscriber[0] == event_name:
                subscriber[1]()
