import customtkinter as ctk

from dune_tournament_scoreboard.gui.app import App

if __name__ == '__main__':
    # Appearance
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    # Display window
    app = App()
    try:
        app.mainloop()
    except KeyboardInterrupt:
        print("Closed by user")
