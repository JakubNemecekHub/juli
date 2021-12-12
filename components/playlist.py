""" Playlist and its frame """

import os
import tkinter as tk

import music_tag

# STARTING_DIR = r"Mike Oldfield/Light And Shade"
STARTING_DIR = r"Blackmores Night/Natures Light (2001)"
FORMATS = [".mp3", ".vaw", ".ogg"]
TAG_NAMES = ["artist", "album", "tracknumber", "tracktitle"]


class Playlist():

    def __init__(self, master):

        self.master = master

        # Playlist
        self.list = {}

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

    def is_selected(self) -> bool:
        return bool(self.box.curselection())

    def get_index(self):
        return self.box.curselection()[0]

    def get_active(self):
        return self.box.get(tk.ACTIVE) # Is it boolean?

    def size(self):
        return self.box.size()

    def clear_selection(self):
        self.box.selection_clear(0, tk.END)
        self.box.see(0)

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
                # Load and process tags -> this can be its own function
                tags = music_tag.load_file(path)
                song = {key: tags[key].value for key in TAG_NAMES if tags[key].value}
                # What if song doesn't have tags?
                # -> Only if song has all the tags from TAG_NAMES, create a new name
                # -> If only one is missiong then use the file name
                if len(song) == len(TAG_NAMES):
                    # All tags found
                    song_id = f"{song['artist']} - {song['album']} - {song['tracknumber']} - {song['tracktitle']}"
                if not song:
                    # At least one tag missing
                    song_id = os.path.splitext(file)[0]
                song["path"] = path
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
        # Populate playlistbox
        self.list = loaded_files.copy()
        for song_id in self.list.keys():
            self.box.insert(tk.END, song_id)

    def loop_continuity(self):
        if self.master.playback_status == self.master.status_enum.PLAYING and not self.master.mixer.get_busy():
            # If at the last song of the playlist -> STOPPED
            current_index = self.get_index()
            if current_index == self.size() - 1:
                self.master.playback_status = self.master.status_enum.STOPPED
            else:
                # Player is playing but the mixer is not busy
                # Not at the last song in playlist
                # -> play next song
                self.master.controls.song_next()

        self.master.root.after(100, self.loop_continuity)

    def double(self, event):
        self.master.controls.song_play()
