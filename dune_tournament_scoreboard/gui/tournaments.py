from tkinter import *
import customtkinter as ctk

from dune_tournament_scoreboard.gui.players import Players
from dune_tournament_scoreboard.gui.rounds import Rounds
from dune_tournament_scoreboard.gui.scoreboard import Scoreboard


# TODO
# List tournaments
# Create tournaments
# Select tournament


class Tournaments(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.label = ctk.CTkLabel(self, text="Tournaments")
        self.label.grid(row=0, column=0, padx=20)


class CurrentTournament(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Configure grid system
        self.grid_rowconfigure(0, weight=1)

        # Add Players
        self.players = Players(self)
        self.grid_columnconfigure(0, weight=1)
        self.players.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        # Add Rounds
        self.rounds = Rounds(self)
        self.grid_columnconfigure(1, weight=1)
        self.rounds.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        # Add Scoreboard
        self.scoreboard = Scoreboard(self)
        self.grid_columnconfigure(2, weight=1)
        self.scoreboard.grid(row=0, column=2, padx=20, pady=20, sticky="nsew")
