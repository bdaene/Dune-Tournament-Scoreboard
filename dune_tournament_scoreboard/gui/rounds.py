import customtkinter as ctk

from dune_tournament_scoreboard.assets.score import Score
from dune_tournament_scoreboard.controllers import tournament
from dune_tournament_scoreboard.gui.event_handler import EventName
from dune_tournament_scoreboard.gui.utils import enter_only_digits


class Rounds(ctk.CTkFrame):
    def __init__(self, master, event_handler, **kwargs):
        super().__init__(master, **kwargs)

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


class RoundsView(ctk.CTkTabview):
    def __init__(self, master, event_handler, **kwargs):
        super().__init__(master, **kwargs)
        self.event_handler = event_handler

        self.configure(anchor="nw")

        integers_only = (self.register(enter_only_digits), '%P', '%d')
        self.default_entry = {"width": 15, "validate": 'key', "validatecommand": integers_only}
        self.default_grid_number = {"padx": 1, "pady": 2, "sticky": "ew"}
        self.default_grid_text = {"padx": 1, "pady": 2, "sticky": "w"}

        for round_index, round in enumerate(tournament.list_rounds()):
            self.add_round(round, round_index + 1)

        # Select last round
        self.select_last_round()

    def select_last_round(self):
        self.set("Ronde {}".format(len(tournament.list_rounds())))

    def add_round(self, round, round_number):
        round_name = "Ronde {}".format(round_number)
        tab_frame = self.add(round_name)
        self._add_round_content(round, tab_frame, round_number)

    def _add_round_content(self, round, tab_frame, round_number):

        # Grid configuration
        tab_frame.grid_columnconfigure(0, weight=1)
        tab_frame.grid_columnconfigure(1, weight=1)
        tab_frame.grid_columnconfigure(2, weight=5)
        tab_frame.grid_columnconfigure(3, weight=0, uniform="same_group")
        tab_frame.grid_columnconfigure(4, weight=0, uniform="same_group")
        tab_frame.grid_columnconfigure(5, weight=0, uniform="same_group")
        tab_frame.grid_columnconfigure(6, weight=0, uniform="same_group")
        tab_frame.grid_columnconfigure(7, weight=0, uniform="same_group")
        tab_frame.grid_columnconfigure(8, weight=0, uniform="same_group")

        # Headers
        tp_header = ctk.CTkLabel(tab_frame, text="PT")
        tp_header.grid(row=0, column=3, **self.default_grid_text)
        vp_header = ctk.CTkLabel(tab_frame, text="PV")
        vp_header.grid(row=0, column=4, **self.default_grid_text)
        spice_header = ctk.CTkLabel(tab_frame, text="Épice")
        spice_header.grid(row=0, column=5, **self.default_grid_text)
        solaris_header = ctk.CTkLabel(tab_frame, text="Solaris")
        solaris_header.grid(row=0, column=6, **self.default_grid_text)
        water_header = ctk.CTkLabel(tab_frame, text="Eau")
        water_header.grid(row=0, column=7, **self.default_grid_text)
        troops_header = ctk.CTkLabel(tab_frame, text="Troupes")
        troops_header.grid(row=0, column=8, **self.default_grid_text)

        # Tables
        row_index = 0
        for table_index, table in enumerate(round.tables):
            separator = ctk.CTkLabel(tab_frame, text="", height=2)
            separator.grid(row=(row_index := row_index + 1), column=0, columnspan=9)
            table_name = ctk.CTkLabel(tab_frame, text="Table {}".format(table_index + 1))
            table_name.grid(row=row_index + 1, column=0, **self.default_grid_text)

            # Players
            for player_index, player_id in enumerate(table):
                row_index += 1
                self._add_player(player_id, player_index, round, row_index, tab_frame, round_number)

    def _add_player(self, player_id, player_index, round, row_index, tab_frame, round_number):
        # Position
        seat_name = ctk.CTkLabel(tab_frame, text="Position {}".format(player_index + 1))
        seat_name.grid(row=row_index, column=1, **self.default_grid_text)

        # Name
        self._add_player_name(player_id, row_index, tab_frame)

        # Score
        tournament_points_variable = ctk.StringVar()
        victory_points_variable = ctk.StringVar()
        spice_variable = ctk.StringVar()
        solaris_variable = ctk.StringVar()
        water_variable = ctk.StringVar()
        troops_variable = ctk.StringVar()

        score = round.scores.get(player_id)
        if score:
            tournament_points_variable.set(score.tournament_points)
            victory_points_variable.set(score.victory_points)
            spice_variable.set(score.spice)
            solaris_variable.set(score.solaris)
            water_variable.set(score.water)
            troops_variable.set(score.troops_in_garrison)

        def _update_player_score(*args):
            if (tournament_points_variable.get()
                    and victory_points_variable.get()
                    and spice_variable.get()
                    and solaris_variable.get()
                    and water_variable.get()
                    and troops_variable.get()):
                tournament.update_score(player_id,
                                        Score(int(tournament_points_variable.get()),
                                              int(victory_points_variable.get()),
                                              int(spice_variable.get()),
                                              int(solaris_variable.get()),
                                              int(water_variable.get()),
                                              int(troops_variable.get())),
                                        round_number - 1)
                self.event_handler.fire(EventName.PLAYER_SCORE_CHANGE, player_id)

        tournament_points_variable.trace_variable('w', _update_player_score)
        victory_points_variable.trace_variable('w', _update_player_score)
        spice_variable.trace_variable('w', _update_player_score)
        solaris_variable.trace_variable('w', _update_player_score)
        water_variable.trace_variable('w', _update_player_score)
        troops_variable.trace_variable('w', _update_player_score)

        # Tournament points
        tournament_points = ctk.CTkEntry(tab_frame, textvariable=tournament_points_variable, **self.default_entry)
        tournament_points.grid(row=row_index, column=3, **self.default_grid_number)

        # Victory points
        victory_points = ctk.CTkEntry(tab_frame, textvariable=victory_points_variable, **self.default_entry)
        victory_points.grid(row=row_index, column=4, **self.default_grid_number)

        # Spice
        spice = ctk.CTkEntry(tab_frame, textvariable=spice_variable, **self.default_entry)
        spice.grid(row=row_index, column=5, **self.default_grid_number)

        # Solaris
        solaris = ctk.CTkEntry(tab_frame, textvariable=solaris_variable, **self.default_entry)
        solaris.grid(row=row_index, column=6, **self.default_grid_number)

        # Water
        water = ctk.CTkEntry(tab_frame, textvariable=water_variable, **self.default_entry)
        water.grid(row=row_index, column=7, **self.default_grid_number)

        # Troops in garrison
        troops = ctk.CTkEntry(tab_frame, textvariable=troops_variable, **self.default_entry)
        troops.grid(row=row_index, column=8, **self.default_grid_number)

    def _add_player_name(self, player_id, row_index, tab_frame):
        player_name = ctk.CTkLabel(tab_frame, text=tournament.get_player(player_id).surname)
        player_name.grid(row=row_index, column=2, **self.default_grid_text)

        def _update_player_name(player_id_event):
            if player_id_event == player_id:
                player_name.configure(text=tournament.get_player(player_id).surname)

        self.event_handler.subscribe(EventName.PLAYER_NAME_CHANGE, _update_player_name)
