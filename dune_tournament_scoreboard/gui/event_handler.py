from enum import Enum
from typing import List, Any


class EventName(Enum):
    PLAYER_NAME_CHANGE = 1
    PLAYER_STATUS_CHANGE = 2
    PLAYER_SCORE_CHANGE = 3
    PLAYER_ADDED = 4


class EventHandler:

    def __init__(self):
        self.subscribers_players = []
        self.subscribers_any_players = []

    def subscribe_player(self, event_name: EventName, player_id, action):
        self.subscribers_players.append((event_name, player_id, action))

    def subscribe_any_player(self, event_name: EventName, action):
        self.subscribers_any_players.append((event_name, action))

    def fire_player(self, event_name: EventName, player_id):
        for subscriber in self.subscribers_players:
            if subscriber[0] == event_name and subscriber[1] == player_id:
                subscriber[2]()
        for subscriber in self.subscribers_any_players:
            if subscriber[0] == event_name:
                subscriber[1]()
