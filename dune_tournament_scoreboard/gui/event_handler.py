from enum import Enum
from typing import List, Any


class EventName(Enum):
    PLAYER_NAME_CHANGE = 1
    PLAYER_STATUS_CHANGE = 2


class EventHandler:

    def __init__(self):
        self.subscribers = []

    def subscribe(self, event_name: EventName, action):
        self.subscribers.append((event_name, action))

    def fire(self, event_name: EventName, *event_values):
        for subscriber in self.subscribers:
            if subscriber[0] == event_name:
                subscriber[1](*event_values)
