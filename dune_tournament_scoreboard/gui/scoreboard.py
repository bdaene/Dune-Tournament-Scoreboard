from tkinter import *
import customtkinter as ctk

from dune_tournament_scoreboard.controllers import tournament
from dune_tournament_scoreboard.gui.event_handler import EventName


# TODO
# Scoreboard (list of players)
#   Player (name + rounds scores (only TP) + cumulated scores)
# Greyed out inactive players


class Scoreboard(ctk.CTkFrame):
    def __init__(self, master, event_handler, **kwargs):
        super().__init__(master, **kwargs)
        self.event_handler = event_handler

        self.label = ctk.CTkLabel(self, text="Scoreboard")
        self.label.grid(row=0, column=0, padx=20)

        for count, player_info in enumerate(tournament.get_summary()):
            self._add_player_row(count, player_info)

    def _add_player_row(self, count, player_info):
        player_name_variable = ctk.StringVar(value=player_info[0].surname)
        player_name = ctk.CTkLabel(self, textvariable=player_name_variable)
        default_color = player_name.cget("text_color")
        if not player_info[0].is_active:
            player_name.configure(text_color="grey")
        player_name.grid(row=count + 1, column=0, padx=5, pady=2, sticky="w")

        self.event_handler.subscribe(EventName.PLAYER_NAME_CHANGE,
                                     lambda: player_name_variable.set(tournament.get_player(player_info[0].id).surname))
        self.event_handler.subscribe(EventName.PLAYER_STATUS_CHANGE,
                                     lambda: player_name.configure(text_color=default_color if tournament.get_player(
                                         player_info[0].id).is_active else "grey"))
