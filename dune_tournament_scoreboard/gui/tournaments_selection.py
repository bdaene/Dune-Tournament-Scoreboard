from tkinter import *
import customtkinter as ctk

from dune_tournament_scoreboard.gui.utils import *


# TODO
# List tournaments
# Create tournaments
# Select tournament

class TournamentSelection(ctk.CTkToplevel):
    def __init__(self, master, display, **kwargs):
        super().__init__(master, **kwargs)
        self.title("Sélection du tournoi")

        def select_tournament(choice):
            print("Tournament selected:", choice)
            display(choice)
            self.destroy()
            self.update()

        def create_tournament():
            dialog = ctk.CTkInputDialog(text="Choisissez un nom de tournoi", title="Créer un tournoi")
            get_input = dialog.get_input()
            print("Tournament name:", get_input)
            select_tournament(get_input)

        # New tournament
        self.tournament_creation_button = ctk.CTkButton(self, text="Créer un nouveau tournoi",
                                                        command=create_tournament)
        self.tournament_creation_button.grid(row=0, column=0, padx=10, pady=10)

        # Existing tournaments
        self.selected_tournament = ctk.StringVar(value="Tournoi 2")  # set initial value
        self.available_tournaments = ctk.CTkOptionMenu(self, values=["Tournoi 1", "Tournoi 2", "Tournoi 3"],
                                                       command=select_tournament,
                                                       variable=self.selected_tournament)
        self.available_tournaments.grid(row=0, column=1, padx=10, pady=10)

        center_frame(self)
