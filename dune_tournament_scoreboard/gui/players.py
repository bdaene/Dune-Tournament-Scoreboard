from tkinter import *
import customtkinter as ctk

from dune_tournament_scoreboard.controllers import tournament


# TODO
# List players
# Add players
# Edit players (name/surname + active)


class Players(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

    def refresh(self):

        # Cleanup
        for grid_slave in self.grid_slaves():
            grid_slave.grid_remove()

        # Title
        title = ctk.CTkLabel(self, text="Joueurs")
        self.grid_columnconfigure(0, weight=1)
        title.grid(row=0, column=0, columnspan=2, padx=20)

        # Players
        players = tournament.list_players()
        for count, player in enumerate(players):
            player_name = ctk.StringVar(value=player.surname)
            is_active = ctk.BooleanVar(value=player.is_active)
            name = ctk.CTkEntry(self, textvariable=player_name, text_color="white" if is_active.get() else "grey")
            name.grid(row=count + 1, column=0, padx=5, pady=2, sticky="ew")
            is_active_switch = ctk.CTkSwitch(self, text="", onvalue=True, offvalue=False, variable=is_active,
                                             command=self._switch_player_status(player=player))
            is_active_switch.grid(row=count + 1, column=1, padx=5, pady=2, sticky="e")

        # Add player button
        create_player_button = ctk.CTkButton(self, text="Ajouter un joueur", command=self._add_player)
        create_player_button.grid(row=len(players) + 1, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

    def _add_player(self):
        dialog = ctk.CTkInputDialog(text="Nom du joueur", title="Ajouter un joueur")
        get_input = dialog.get_input()
        tournament.create_player("", get_input)
        self.refresh()

    def _switch_player_status(self, player):
        return lambda: self._switch_status(player)

    def _switch_status(self, player):
        tournament.switch_player_status(player.id, not player.is_active)
        self.refresh()
