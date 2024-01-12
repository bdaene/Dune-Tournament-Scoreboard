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
        self.event_handler.subscribe_any_player(EventName.PLAYER_SCORE_CHANGE, self._refresh)
        self.event_handler.subscribe_any_player(EventName.PLAYER_ADDED, self._refresh)
        self.default_grid_text = {"padx": 1, "pady": 2, "sticky": "w"}
        self._refresh()

    def _refresh(self):

        # Cleanup
        for grid_slave in self.grid_slaves():
            grid_slave.grid_remove()

        # Grid configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0, uniform="same_group")
        self.grid_columnconfigure(2, weight=0, uniform="same_group")
        self.grid_columnconfigure(3, weight=0, uniform="same_group")
        self.grid_columnconfigure(4, weight=0, uniform="same_group")
        self.grid_columnconfigure(5, weight=0, uniform="same_group")
        self.grid_columnconfigure(6, weight=0, uniform="same_group")
        self.grid_columnconfigure(7, weight=0, uniform="same_group")

        # Title
        label = ctk.CTkLabel(self, text="Scoreboard")
        label.grid(row=0, column=0, padx=20)

        # Headers
        tp_header = ctk.CTkLabel(self, text="PT")
        tp_header.grid(row=1, column=1, **self.default_grid_text)
        vp_header = ctk.CTkLabel(self, text="PV")
        vp_header.grid(row=1, column=2, **self.default_grid_text)
        spice_header = ctk.CTkLabel(self, text="Épice")
        spice_header.grid(row=1, column=3, **self.default_grid_text)
        solaris_header = ctk.CTkLabel(self, text="Solaris")
        solaris_header.grid(row=1, column=4, **self.default_grid_text)
        water_header = ctk.CTkLabel(self, text="Eau")
        water_header.grid(row=1, column=5, **self.default_grid_text)
        troops_header = ctk.CTkLabel(self, text="Troupes")
        troops_header.grid(row=1, column=6, **self.default_grid_text)

        # Players
        for count, player_info in enumerate(tournament.get_summary()):
            self._add_player_row(count + 2, player_info)

    def _add_player_row(self, row_index, player_info):
        self._add_player_name(row_index, player_info)

        # Score
        self._add_scores(player_info, row_index)

    def _add_scores(self, player_info, row_index):
        player_score = player_info[2]
        # Tournament points
        tournament_points = ctk.CTkLabel(self, text=player_score.tournament_points, width=15)
        tournament_points.grid(row=row_index, column=1, **self.default_grid_text)
        # Victory points
        victory_points = ctk.CTkLabel(self, text=player_score.victory_points, width=15)
        victory_points.grid(row=row_index, column=2, **self.default_grid_text)
        # Spice
        spice = ctk.CTkLabel(self, text=player_score.spice, width=15)
        spice.grid(row=row_index, column=3, **self.default_grid_text)
        # Solaris
        solaris = ctk.CTkLabel(self, text=player_score.solaris, width=15)
        solaris.grid(row=row_index, column=4, **self.default_grid_text)
        # Water
        water = ctk.CTkLabel(self, text=player_score.water, width=15)
        water.grid(row=row_index, column=5, **self.default_grid_text)
        # Troops in garrison
        troops = ctk.CTkLabel(self, text=player_score.troops_in_garrison, width=15)
        troops.grid(row=row_index, column=6, **self.default_grid_text)

    def _add_player_name(self, row_index, player_info):
        player_name_variable = ctk.StringVar(value=player_info[0].surname)
        player_name = ctk.CTkLabel(self, textvariable=player_name_variable)
        default_color = player_name.cget("text_color")
        if not player_info[0].is_active:
            player_name.configure(text_color="grey")
        player_name.grid(row=row_index, column=0, padx=5, pady=2, sticky="w")
        self.event_handler.subscribe_player(EventName.PLAYER_NAME_CHANGE, player_info[0].id,
                                            lambda: player_name_variable.set(
                                                tournament.get_player(player_info[0].id).surname))
        self.event_handler.subscribe_player(EventName.PLAYER_STATUS_CHANGE, player_info[0].id,
                                            lambda: player_name.configure(
                                                text_color=default_color if tournament.get_player(
                                                    player_info[0].id).is_active else "grey"))
