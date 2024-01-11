import customtkinter as ctk

from dune_tournament_scoreboard.gui.players import Players
from dune_tournament_scoreboard.gui.rounds import Rounds
from dune_tournament_scoreboard.gui.scoreboard import Scoreboard
from dune_tournament_scoreboard.gui.tournaments_selection import TournamentSelection
from dune_tournament_scoreboard.gui.utils import center_frame


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.withdraw()

        # Select tournament
        self.tournament_selection = TournamentSelection(self, self.display)

        # Create other variables
        self.players = Players(self)
        self.rounds = Rounds(self)
        self.scoreboard = Scoreboard(self)

    def display(self, tournament_choice):
        self.title('Dune Tournament Scoreboard - ' + tournament_choice)

        # Configure grid system
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.configure(padx=10, pady=10)

        # Add Players
        self.players.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        # Add Rounds
        self.rounds.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        # Add Scoreboard
        self.scoreboard.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")

        # Size and position
        bind_fullscreen_keys(self)
        set_size_ratio(self, 0.9, 0.8)
        center_frame(self)


def set_size_ratio(frame, width_ratio, height_ratio):
    frame.geometry(
        '{}x{}'.format(int(frame.winfo_screenwidth() * width_ratio), int(frame.winfo_screenheight() * height_ratio)))


def bind_fullscreen_keys(frame):
    frame.bind("<F11>",
               lambda event: frame.attributes("-fullscreen", not frame.attributes("-fullscreen")))
    frame.bind("<Escape>", lambda event: frame.attributes("-fullscreen", False))
