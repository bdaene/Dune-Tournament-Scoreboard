import customtkinter as ctk

from dune_tournament_scoreboard.controllers import tournament
from dune_tournament_scoreboard.gui.event_handler import EventName


class Players(ctk.CTkFrame):
    def __init__(self, master, event_handler, **kwargs):
        super().__init__(master, **kwargs)
        self.event_handler = event_handler
        self.event_handler.subscribe_any_player(EventName.PLAYER_ADDED, self.refresh)
        self.refresh()

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
            self._add_player_row(count, player)

        # Add player button
        add_player_button = ctk.CTkButton(self, text="Ajouter un joueur", command=self._add_new_player)
        add_player_button.grid(row=len(players) + 1, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

    def _add_player_row(self, count, player):
        player_name = ctk.StringVar(value=player.surname)
        player_name.trace_variable('w', self._update_player_surname(player=player, player_name=player_name))

        name = ctk.CTkEntry(self, textvariable=player_name)
        default_color = name.cget("text_color")
        if not player.is_active:
            name.configure(text_color="grey")
        name.grid(row=count + 1, column=0, padx=5, pady=2, sticky="ew")

        is_active = ctk.BooleanVar(value=player.is_active)
        is_active.trace_variable('w', self._switch_player_status(player=player, entry_name=name,
                                                                 default_color=default_color))

        is_active_switch = ctk.CTkSwitch(self, text="", onvalue=True, offvalue=False, variable=is_active)
        is_active_switch.grid(row=count + 1, column=1, padx=5, pady=2, sticky="e")

    def _add_new_player(self):
        dialog = ctk.CTkInputDialog(text="Nom du joueur", title="Ajouter un joueur")
        get_input = dialog.get_input()
        if get_input:
            tournament.create_player("", get_input)
            self.event_handler.fire_player(EventName.PLAYER_ADDED, "")

    def _update_player_surname(self, player, player_name):
        return lambda *args: self._update_player_surname_and_register(player, player_name)

    def _update_player_surname_and_register(self, player, player_name):
        player.surname = player_name.get()
        tournament.update_player(player)
        self.event_handler.fire_player(EventName.PLAYER_NAME_CHANGE, player.id)

    def _switch_player_status(self, player, entry_name, default_color):
        return lambda *args: self._switch_status(player, entry_name, default_color)

    def _switch_status(self, player, entry_name, default_color):
        tournament.switch_player_status(player.id, not player.is_active)
        entry_name.configure(text_color=default_color if player.is_active else "grey")
        self.event_handler.fire_player(EventName.PLAYER_STATUS_CHANGE, player.id)
