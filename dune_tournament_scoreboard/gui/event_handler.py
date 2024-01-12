from enum import Enum
from typing import List, Any


class EventName(Enum):
    PLAYER_NAME_CHANGE = 1
    PLAYER_STATUS_CHANGE = 2
    PLAYER_SCORE_CHANGE = 3


class EventHandler:

    def __init__(self):
        self.subscribers = []

    def subscribe(self, event_name: EventName, player_id, action):
        self.subscribers.append((event_name, player_id, action))

    def fire(self, event_name: EventName, player_id):
        for subscriber in self.subscribers:
            if subscriber[0] == event_name and subscriber[1] == player_id:
                subscriber[2]()
