from tkinter import *
import customtkinter as ctk


# TODO
# Create rounds
# Select the view on a specific round
# View round (set of tables)
# View table (list of 3-4 seats)
#   Table number
# View seat
#   Seat number
#   Player
#   Score


class Rounds(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.label = ctk.CTkLabel(self, text="Rounds")
        self.label.grid(row=0, column=0, padx=20)
