def center_frame(frame):
    frame.deiconify()  # Needed to make sure winfo_width and winfo_height are already set and not the default 200 200

    # Set position
    scale_factor = frame._get_window_scaling()
    width = frame.winfo_width()
    height = frame.winfo_height() + frame.winfo_rooty() - frame.winfo_y()  # Titlebar to take into account
    pos_x_centered = int(frame.winfo_screenwidth() / 2 * scale_factor - width / 2)
    pos_y_centered = int(frame.winfo_screenheight() / 2 * scale_factor - height / 2)
    frame.geometry(f"+{pos_x_centered}+{pos_y_centered}")
    frame.deiconify()


def set_size_ratio(frame, width_ratio, height_ratio):
    frame.geometry(f"{int(frame.winfo_screenwidth() * width_ratio)}x{int(frame.winfo_screenheight() * height_ratio)}")


def bind_fullscreen_keys(frame):
    frame.bind("<F11>", lambda event: frame.attributes("-fullscreen", not frame.attributes("-fullscreen")))
    frame.bind("<Escape>", lambda event: frame.attributes("-fullscreen", False))


def enter_only_digits(entry, action_type) -> bool:
    if action_type == '1' and not entry.isdigit():
        return False
    return True
