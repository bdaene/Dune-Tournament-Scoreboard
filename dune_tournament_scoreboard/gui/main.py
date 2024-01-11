from tkinter import *
import customtkinter as ctk


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


if __name__ == '__main__':
    app = ctk.CTk()

    # Appearance
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    app.title('Dune Tournament Scoreboard')

    # Dummy label
    label = ctk.CTkLabel(master=app, text="Dummy label")
    label.pack(padx=5, pady=5)

    # Size and position
    bind_fullscreen_keys(app)
    set_size_ratio(app, 0.9, 0.8)
    center_frame(app)

    # Display window
    try:
        app.mainloop()
    except KeyboardInterrupt:
        print("Closed by user")
