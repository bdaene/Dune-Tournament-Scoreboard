import customtkinter as ctk
from attr import astuple

from dune_tournament_scoreboard.controllers import tournament
from dune_tournament_scoreboard.gui.event_handler import EventName


class Scoreboard(ctk.CTkFrame):
    def __init__(self, master, event_handler, **kwargs):
        super().__init__(master, **kwargs)
        self.event_handler = event_handler
        self.events_to_unsubscribe = []
        self.event_handler.subscribe_global(EventName.PLAYER_SCORE_CHANGE, self._refresh)
        self.event_handler.subscribe_global(EventName.PLAYER_ADDED, self._refresh)
        self.event_handler.subscribe_global(EventName.NEW_ROUND, self._refresh)
        self.default_grid_text = {"padx": 3, "pady": 2, "sticky": "e"}
        self._refresh()

    def _refresh(self):

        # Cleanup
        for grid_slave in self.grid_slaves():
            for key in self.events_to_unsubscribe:
                self.event_handler.unsubscribe_player(key)
            self.events_to_unsubscribe.clear()
            grid_slave.grid_remove()
            grid_slave.destroy()

        summary = tournament.get_summary()
        total_rounds = 0 if len(summary) == 0 else len(summary[0][1])

        # Grid configuration
        self.grid_columnconfigure(0, weight=1)
        for i in range(1, total_rounds + 7):
            self.grid_columnconfigure(i, weight=0, uniform="same_group")

        # Title
        label = ctk.CTkLabel(self, text="Classement")
        label.grid(row=0, column=0, columnspan=total_rounds + 7, padx=20)

        # Headers
        for i in range(total_rounds):
            ctk.CTkLabel(self, text="Ronde {}".format(i + 1)).grid(row=1, column=i + 1, **self.default_grid_text)
        for column, label in enumerate(("PT", "PV", "Épice", "Solaris", "Eau", "Troupes"), total_rounds + 1):
            ctk.CTkLabel(self, text=label).grid(row=1, column=column, **self.default_grid_text)

        # Players
        for row, player_info in enumerate(summary, 2):
            self._add_player_row(row, player_info)

    def _add_player_row(self, row_index, player_info):
        self._add_player_name(row_index, player_info)

        # Score
        self._add_scores(player_info, row_index)

    def _add_scores(self, player_info, row_index):
        player, tournament_points, score = player_info

        # Rounds
        total_rounds = len(tournament_points)
        for column, round_tournament_points in enumerate(tournament_points, 1):
            ctk.CTkLabel(self, text=round_tournament_points).grid(row=row_index, column=column,
                                                                  **self.default_grid_text)

        # Total score
        for column, value in enumerate(astuple(score), total_rounds + 1):
            ctk.CTkLabel(self, text=value).grid(row=row_index, column=column, **self.default_grid_text)

    def _add_player_name(self, row_index, player_info):
        player_name_variable = ctk.StringVar(value=player_info[0].surname)
        player_name = ctk.CTkLabel(self, textvariable=player_name_variable, anchor="w")
        default_color = player_name.cget("text_color")
        if not player_info[0].is_active:
            player_name.configure(text_color="grey")
        player_name.grid(row=row_index, column=0, padx=5, pady=2, sticky="ew")
        self.events_to_unsubscribe.append(
            self.event_handler.subscribe_player(EventName.PLAYER_NAME_CHANGE, player_info[0].id,
                                                lambda: player_name_variable.set(
                                                    tournament.get_player(player_info[0].id).surname)))
        self.events_to_unsubscribe.append(
            self.event_handler.subscribe_player(EventName.PLAYER_STATUS_CHANGE, player_info[0].id,
                                                lambda: player_name.configure(
                                                    text_color=default_color if tournament.get_player(
                                                        player_info[0].id).is_active else "grey")))
