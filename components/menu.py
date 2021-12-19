""" Menu """
import typing


import tkinter as tk
from tkinter import filedialog


class Menu():

    def __init__(self, root: tk.Tk, open_folder: typing.Callable, add_folder: typing.Callable, add_songs: typing.Callable):

        self.root = root

        menu_bar = tk.Menu(root)
        # File Menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Open Folder", command=open_folder)
        file_menu.add_command(label="Add Folder", command=add_folder)
        file_menu.add_command(label="Add Songs", command=add_songs)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.menu_exit)
        # Other Menus
        # ...
        # Add menus to menu bar
        menu_bar.add_cascade(label="File", menu=file_menu)
        root.config(menu=menu_bar)

    def menu_exit(self):
        self.root.destroy()
