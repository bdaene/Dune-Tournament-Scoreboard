import customtkinter as ctk

from dune_tournament_scoreboard.controllers import tournament
from dune_tournament_scoreboard.gui.event_handler import EventHandler
from dune_tournament_scoreboard.gui.players import Players
from dune_tournament_scoreboard.gui.rounds import Rounds
from dune_tournament_scoreboard.gui.scoreboard import Scoreboard
from dune_tournament_scoreboard.gui.tournaments_selection import TournamentSelection
from dune_tournament_scoreboard.gui.utils import center_frame, set_size_ratio, bind_fullscreen_keys


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.withdraw()

        # Select tournament
        self.tournament_selection = TournamentSelection(self, self._display)

    def _display(self):
        self.title('Dune Tournament Scoreboard - ' + tournament.get_current())

        # Configure grid system
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_columnconfigure(2, weight=2)
        self.configure(padx=10, pady=10)

        # Create event handler
        event_handler = EventHandler()

        # Add Players
        players = Players(self, event_handler=event_handler)
        players.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        # Add Rounds
        rounds = Rounds(self, event_handler=event_handler)
        rounds.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        # Add Scoreboard
        scoreboard = Scoreboard(self, event_handler=event_handler)
        scoreboard.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")

        # Size and position
        bind_fullscreen_keys(self)
        set_size_ratio(self, 0.9, 0.8)
        center_frame(self)
