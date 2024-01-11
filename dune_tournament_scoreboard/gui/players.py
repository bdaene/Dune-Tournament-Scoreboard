from tkinter import *
import customtkinter as ctk


# TODO
# List players
# Add players
# Edit players (name/surname + active)


class Players(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.label = ctk.CTkLabel(self, text="Players")
        self.label.grid(row=0, column=0, padx=20)
