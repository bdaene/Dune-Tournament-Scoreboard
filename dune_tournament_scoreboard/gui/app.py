import customtkinter as ctk

from dune_tournament_scoreboard.gui.tournaments import Tournaments, CurrentTournament


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title('Dune Tournament Scoreboard')

        # Add Tournaments
        self.tournaments = Tournaments(self)
        self.tournaments.pack(side="top", fill="x")

        # Add current tournament
        self.currentTournament = CurrentTournament(self)
        self.currentTournament.pack(fill="both", expand=True)

        # Size and position
        bind_fullscreen_keys(self)
        set_size_ratio(self, 0.9, 0.8)
        center_frame(self)


def center_frame(frame):
    frame.deiconify()  # Needed to make sure winfo_width and winfo_height are already set and not the default 200 200

    # Set position
    scale_factor = frame._get_window_scaling()
    width = frame.winfo_width()
    height = frame.winfo_height() + frame.winfo_rooty() - frame.winfo_y()  # Titlebar to take into account
    pos_x_centered = int(frame.winfo_screenwidth() / 2 * scale_factor - width / 2)
    pos_y_centered = int(frame.winfo_screenheight() / 2 * scale_factor - height / 2)
    frame.geometry('+{}+{}'.format(pos_x_centered, pos_y_centered))
    frame.deiconify()


def set_size_ratio(frame, width_ratio, height_ratio):
    frame.geometry(
        '{}x{}'.format(int(frame.winfo_screenwidth() * width_ratio), int(frame.winfo_screenheight() * height_ratio)))


def bind_fullscreen_keys(frame):
    frame.bind("<F11>",
               lambda event: frame.attributes("-fullscreen", not frame.attributes("-fullscreen")))
    frame.bind("<Escape>", lambda event: frame.attributes("-fullscreen", False))
