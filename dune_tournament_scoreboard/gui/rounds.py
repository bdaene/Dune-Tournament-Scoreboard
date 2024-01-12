import customtkinter as ctk
from attr import astuple, fields

from dune_tournament_scoreboard.assets.score import Score
from dune_tournament_scoreboard.controllers import tournament
from dune_tournament_scoreboard.gui.event_handler import EventName
from dune_tournament_scoreboard.gui.utils import enter_only_digits


class Rounds(ctk.CTkFrame):
    def __init__(self, master, event_handler, **kwargs):
        super().__init__(master, **kwargs)
        self.event_handler = event_handler

        # Title
        title = ctk.CTkLabel(self, text="Rondes")
        self.grid_columnconfigure(0, weight=1)
        title.grid(row=0, column=0, padx=20)

        # Rounds
        self.rounds_view = RoundsView(self, event_handler)
        self.rounds_view.grid(row=1, column=0, padx=5, sticky="ew")

        # Add round button
        add_round_button = ctk.CTkButton(self, text="Nouvelle ronde", command=self._add_round)
        add_round_button.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

    def _add_round(self):
        tournament.create_new_round()
        rounds = tournament.list_rounds()
        self.rounds_view.add_round(rounds[-1], len(rounds))
        self.rounds_view.select_last_round()
        self.event_handler.fire_global(EventName.NEW_ROUND)


class RoundsView(ctk.CTkTabview):
    def __init__(self, master, event_handler, **kwargs):
        super().__init__(master, **kwargs)
        self.event_handler = event_handler

        self.configure(anchor="nw")

        integers_only = (self.register(enter_only_digits), '%P', '%d')
        self.default_entry = {"width": 15, "validate": 'key', "validatecommand": integers_only}
        self.default_grid_number = {"padx": 1, "pady": 2, "sticky": "ew"}
        self.default_grid_text = {"padx": 1, "pady": 2, "sticky": "w"}

        for round_index, round_ in enumerate(tournament.list_rounds(), 1):
            self.add_round(round_, round_index)

        self.select_last_round()

    def select_last_round(self):
        last_round = len(tournament.list_rounds())
        if last_round > 0:
            self.set(f"Ronde {last_round}")

    def add_round(self, round, round_number):
        round_name = "Ronde {}".format(round_number)
        tab_frame = self.add(round_name)
        self._add_round_content(round, tab_frame, round_number)

    def _add_round_content(self, round, tab_frame, round_number):

        # Grid configuration
        tab_frame.grid_columnconfigure(0, weight=1)
        tab_frame.grid_columnconfigure(1, weight=1)
        tab_frame.grid_columnconfigure(2, weight=5)
        for i in range(3, 9):
            tab_frame.grid_columnconfigure(i, weight=0, uniform="same_group")

        # Headers
        for i, label in enumerate(("PT", "PV", "Épice", "Solaris", "Eau", "Troupes"), 3):
            ctk.CTkLabel(tab_frame, text=label).grid(row=0, column=i, **self.default_grid_text)

        # Tables
        row_index = 0
        for table_index, table in enumerate(round.tables, 1):
            row_index += 1
            separator = ctk.CTkLabel(tab_frame, text="", height=2)
            separator.grid(row=row_index, column=0, columnspan=9)
            table_name = ctk.CTkLabel(tab_frame, text=f"Table {table_index}")
            table_name.grid(row=row_index + 1, column=0, **self.default_grid_text)

            # Players
            for seat, player_id in enumerate(table, 1):
                row_index += 1
                self._add_player(player_id, seat, round, row_index, tab_frame, round_number)

    def _add_player(self, player_id, seat, round_, row_index, tab_frame, round_number):
        # Position
        seat_name = ctk.CTkLabel(tab_frame, text=f"Position {seat}")
        seat_name.grid(row=row_index, column=1, **self.default_grid_text)

        # Name
        self._add_player_name(player_id, row_index, tab_frame)

        # Score
        scores_variables = [ctk.StringVar() for _ in fields(Score)]

        score = round_.scores.get(player_id)
        if score:
            for variable, value in zip(scores_variables, astuple(score)):
                variable.set(value)

        def _update_player_score(*args):
            if all(variable_.get() for variable_ in scores_variables):
                tournament.update_score(player_id,
                                        Score(*(int(variable_.get()) for variable_ in scores_variables)),
                                        round_number - 1)
                self.event_handler.fire_player(EventName.PLAYER_SCORE_CHANGE, player_id)

        for column, variable in enumerate(scores_variables, 3):
            variable.trace_variable('w', _update_player_score)
            entry = ctk.CTkEntry(tab_frame, textvariable=variable, **self.default_entry)
            entry.grid(row=row_index, column=column, **self.default_grid_number)

    def _add_player_name(self, player_id, row_index, tab_frame):
        player_name_variable = ctk.StringVar(value=tournament.get_player(player_id).surname)
        player_name = ctk.CTkLabel(tab_frame, textvariable=player_name_variable)
        player_name.grid(row=row_index, column=2, **self.default_grid_text)

        self.event_handler.subscribe_player(EventName.PLAYER_NAME_CHANGE, player_id,
                                            lambda: player_name_variable.set(tournament.get_player(player_id).surname))
