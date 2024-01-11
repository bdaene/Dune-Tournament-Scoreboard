from tkinter import *
import customtkinter as ctk

from dune_tournament_scoreboard.controllers import tournament
from dune_tournament_scoreboard.gui.utils import *


class TournamentSelection(ctk.CTkToplevel):
    def __init__(self, master, display, **kwargs):
        super().__init__(master, **kwargs)
        self.title("Sélection du tournoi")

        def select_tournament(choice):
            tournament.select(choice)
            display()
            self.destroy()
            self.update()

        def create_tournament():
            dialog = ctk.CTkInputDialog(text="Choisissez un nom de tournoi", title="Créer un tournoi")
            get_input = dialog.get_input()
            tournament.create(get_input)
            select_tournament(get_input)

        # New tournament
        tournament_creation_button = ctk.CTkButton(self, text="Créer un nouveau tournoi",
                                                   command=create_tournament)
        tournament_creation_button.grid(row=0, column=0, padx=10, pady=10)

        # Existing tournaments
        tournaments = [element.replace('_', ' ') for element in tournament.list_tournaments()]
        if tournaments:
            selected_tournament = ctk.StringVar(value="Choisissez un tournoi existant")
            available_tournaments = ctk.CTkOptionMenu(self, values=tournaments,
                                                      command=select_tournament,
                                                      variable=selected_tournament)
            available_tournaments.grid(row=0, column=1, padx=10, pady=10)

        center_frame(self)
