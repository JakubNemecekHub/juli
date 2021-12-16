""" Playlist and its frame """

import os
import tkinter as tk

from .tag.tag import get_tags

# STARTING_DIR = r"Mike Oldfield/Light And Shade"
STARTING_DIR = r"Blackmores Night/Natures Light (2001)"
FORMATS = [".mp3", ".vaw", ".ogg"]
# TAG_NAMES = ["artist", "album", "tracknumber", "tracktitle"]


class Playlist():

    def __init__(self, master):

        self.master = master

        # Playlist
        self.list = {}
        self.active_song_index = -1

        # Playlist Frame
        frame_playlist = tk.LabelFrame(self.master.root, text="Playlist", relief=tk.FLAT)
        frame_playlist.place(x=600, y=0, width=400, height=300)
        scroll_y_playlist = tk.Scrollbar(frame_playlist, orient=tk.VERTICAL)
        self.box = tk.Listbox(frame_playlist, yscrollcommand=scroll_y_playlist.set, selectmode=tk.SINGLE, height=16)
        scroll_y_playlist.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_y_playlist.config(command=self.box.yview)
        self.box.pack(fill=tk.BOTH)
        # Set up left mouse double click
        self.box.bind("<Double-1>", self.double)

        # Initial population
        self.populate(os.path.join(self.master.INITIAL_DIR, STARTING_DIR))

    def select(self, index: int):
        # Clear current selection
        if self.box.curselection():
            current_index = self.box.curselection()[0]
            self.box.selection_clear(current_index)
        # Set new selection
        self.box.activate(index)
        self.box.selection_set(index)
        self.box.see(index)
        # Store index of active song, because box is not reliable
        # How to check if above code was succesfull?
        if index < self.box.size():
            self.active_song_index = index
        else:
            self.active_song_index = -1 # What exactly to do here? 

    def is_selected(self) -> bool:
        return bool(self.box.curselection())

    def get_index(self):
        return self.active_song_index 

    def get_active(self):
        return self.box.get(tk.ACTIVE)

    def size(self):
        return self.box.size()

    def clear_selection(self):
        self.box.selection_clear(0, tk.END)
        self.box.see(0)
        self.active_song_index = -1

    def add(self, item):
        # TO DO: parse song tags and update the list
        self.box.insert(tk.END, item)

    def populate(self, folder: str, append = False):
        # Load files
        loaded_files = {}
        for root_dir, dirs, files in os.walk(folder):
            for file in files:
                # Skip non-supported formats
                if os.path.splitext(file)[1] not in FORMATS:
                    continue
                path = os.path.join(root_dir, file)
                song_id, song = get_tags(path)
                loaded_files[song_id] = song
        # Check if any songs loaded
        if not loaded_files:
            # No supported songs founds
            self.master.status_bar.set_files_status("No files found")
            self.master.root.after(3000, lambda : self.master.status_bar.set_files_status(""))
            return
        # Delete present songs if not append
        if not append:
            self.list.clear()           # playlist
            self.box.delete(0, tk.END)  # playlistbox
        # Populate playlistbox with sorted songs
        self.list = dict(sorted(loaded_files.items(), key = lambda item: item[0])) # Is it slow?
        for song_id in self.list.keys():
            self.box.insert(tk.END, song_id)

    def loop_continuity(self):
        if self.master.playback_status == self.master.status_enum.PLAYING and not self.master.mixer.get_busy():
            # If at the last song of the playlist -> STOPPED
            current_index = self.get_index()    # The problem lays here
            if current_index == self.size() - 1:
                self.master.playback_status = self.master.status_enum.STOPPED
            else:
                # Player is playing but the mixer is not busy
                # Not at the last song in playlist
                # -> play next song
                self.master.controls.song_next()

        self.master.root.after(100, self.loop_continuity)

    def double(self, event):
        self.active_song_index = self.box.curselection()[0]
        self.master.controls.song_play()
