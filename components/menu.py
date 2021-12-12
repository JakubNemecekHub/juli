""" Menu """

import tkinter as tk
from tkinter import filedialog


class Menu():

    def __init__(self, master):

        self.master = master

        menu_bar = tk.Menu(self.master.root)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Open Folder", command=self.menu_open_folder)
        file_menu.add_command(label="Add Folder", command=self.menu_add_folder)
        file_menu.add_command(label="Add Songs", command=self.menu_add_songs)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.menu_exit)
        menu_bar.add_cascade(label="File", menu=file_menu)
        self.master.root.config(menu=menu_bar)

    def menu_exit(self):
        self.root.destroy()

    def menu_open_folder(self):
        dir = filedialog.askdirectory(initialdir=self.master.INITIAL_DIR, title="Select a folder")
        if dir:
            # Directory selected
            self.master.controls.song_stop()    # Stop playing
            self.master.playlist.populate(dir)

    def menu_add_folder(self):
        dir = filedialog.askdirectory(initialdir=self.master.INITIAL_DIR, title="Select a folder")
        if dir:
            # Directory selected
            self.master.playlist.populate(dir, append=True)

    def menu_add_songs(self):
        FILE_TYPES = [("Music format", ".mp3"), ("Music format", ".vaw"), ("Music format", ".ogg")]
        selection = filedialog.askopenfilenames(initialdir=self.master.INITIAL_DIR, title="Select a song", filetypes=FILE_TYPES)
        for song in selection:
            self.master.playlist.add(song)