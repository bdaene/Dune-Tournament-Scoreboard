from tkinter import *
import customtkinter as ctk

from dune_tournament_scoreboard.controllers import tournament
from dune_tournament_scoreboard.gui.utils import *


class TournamentSelection(ctk.CTkToplevel):
    def __init__(self, master, display_app, **kwargs):
        super().__init__(master, **kwargs)
        self.title("Sélection du tournoi")

        # Save display function
        self.display_app = display_app

        # New tournament
        tournament_creation_button = ctk.CTkButton(self, text="Créer un nouveau tournoi",
                                                   command=self._create_tournament)
        tournament_creation_button.grid(row=0, column=0, padx=10, pady=10)

        # Existing tournaments
        tournaments = [element.replace('_', ' ') for element in tournament.list_tournaments()]
        if tournaments:
            selected_tournament = ctk.StringVar(value="Choisissez un tournoi existant")
            available_tournaments = ctk.CTkOptionMenu(self, values=tournaments, command=self._select_tournament,
                                                      variable=selected_tournament)
            available_tournaments.grid(row=0, column=1, padx=10, pady=10)

        center_frame(self)

        # If the user close the tournament selection, it should exit the program
        self.wm_protocol("WM_DELETE_WINDOW", lambda: exit(0))

    def _select_tournament(self, choice):
        tournament.select(choice)
        self.display_app()
        self.destroy()
        self.update()

    def _create_tournament(self):
        dialog = ctk.CTkInputDialog(text="Choisissez un nom de tournoi", title="Créer un tournoi")
        get_input = dialog.get_input()
        if get_input:
            tournament.create(get_input)
            self._select_tournament(get_input)
