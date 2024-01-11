from tkinter import *
import customtkinter as ctk


# TODO
# Scoreboard (list of players)
#   Player (name + rounds scores (only TP) + cumulated scores)
# Greyed out inactive players


class Scoreboard(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.label = ctk.CTkLabel(self, text="Scoreboard")
        self.label.grid(row=0, column=0, padx=20)
