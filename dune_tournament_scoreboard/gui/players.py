import customtkinter as ctk

from dune_tournament_scoreboard.controllers import tournament
from dune_tournament_scoreboard.gui.event_handler import EventName, event_handler


class Players(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        event_handler.subscribe_global(EventName.PLAYER_ADDED, self._refresh)
        self._refresh()

    def _refresh(self):

        # Cleanup
        for grid_slave in self.grid_slaves():
            grid_slave.grid_remove()
            grid_slave.destroy()

        # Title
        title = ctk.CTkLabel(self, text="Joueurs")
        self.grid_columnconfigure(0, weight=1)
        title.grid(row=0, column=0, columnspan=2, padx=20)

        # Players
        players = tournament.list_players()
        for count, player in enumerate(players):
            self._add_player_row(count, player)

        # Add player button
        add_player_button = ctk.CTkButton(self, text="Ajouter un joueur", command=_add_new_player)
        add_player_button.grid(row=len(players) + 1, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

    def _add_player_row(self, count, player):
        player_name = ctk.StringVar(value=player.surname)
        player_name.trace_variable('w', _update_player_surname(player=player, player_name=player_name))

        name = ctk.CTkEntry(self, textvariable=player_name)
        default_color = name.cget("text_color")
        if not player.is_active:
            name.configure(text_color="grey")
        name.grid(row=count + 1, column=0, padx=5, pady=2, sticky="ew")

        is_active = ctk.BooleanVar(value=player.is_active)
        is_active.trace_variable('w', _switch_player_status(player=player, entry_name=name,
                                                            default_color=default_color))

        is_active_switch = ctk.CTkSwitch(self, text="", onvalue=True, offvalue=False, variable=is_active)
        is_active_switch.grid(row=count + 1, column=1, padx=5, pady=2, sticky="e")


def _add_new_player():
    dialog = ctk.CTkInputDialog(text="Nom du joueur", title="Ajouter un joueur")
    get_input = dialog.get_input()
    if get_input:
        tournament.create_player("", get_input)
        event_handler.fire_global(EventName.PLAYER_ADDED)


def _update_player_surname(player, player_name):
    def _update_player_surname_and_register(*_):
        player.surname = player_name.get()
        tournament.update_player(player)
        event_handler.fire_player(EventName.PLAYER_NAME_CHANGE, player.id)

    return _update_player_surname_and_register


def _switch_player_status(player, entry_name, default_color):
    def _switch_status(*_):
        tournament.set_player_status(player.id, not player.is_active)
        entry_name.configure(text_color=default_color if player.is_active else "grey")
        event_handler.fire_player(EventName.PLAYER_STATUS_CHANGE, player.id)

    return _switch_status
