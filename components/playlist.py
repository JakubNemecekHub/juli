""" Playlist and its frame """

import os
import tkinter as tk
import typing

import music_tag
import mutagen

FORMATS = [".mp3", ".vaw", ".ogg"] # Should move to mixer


class Song():

    def __init__(self, song: dict):
        self.id = song["id"]
        self.artist = song["artist"]
        self.album = song["album"]
        self.tracknumber = song["tracknumber"]
        self.tracktitle = song["tracktitle"]
        self.duration = song["duration"]
        self.path = song["path"]

    def __str__(self):
        return self.id


class PlaylistBox():

    def __init__(self, double_click: typing.Callable):
        # Playlist Frame
        self.frame = tk.LabelFrame(relief=tk.FLAT) 
        # frame_playlist.place(x=600, y=0, width=400, height=300)
        # frame.pack(fill=tk.X)
        scroll_y_playlist = tk.Scrollbar(self.frame, orient=tk.VERTICAL)
        self.box = tk.Listbox(self.frame, yscrollcommand=scroll_y_playlist.set, selectmode=tk.SINGLE, height=16)
        scroll_y_playlist.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_y_playlist.config(command=self.box.yview)
        self.box.pack(fill=tk.BOTH)
        # Set up left mouse double click
        self.box.bind("<Double-1>", double_click)

    def get_index(self) -> int:
        try:
            return self.box.curselection()[0]
        except IndexError:
            return None

    def select(self, index: int) -> None:
        """ Activates next item in box. """
        # Deselect current selection
        self.box.selection_clear(0, tk.END)
        # Make new selection
        self.box.activate(index)
        self.box.selection_set(index)
        self.box.see(index)

    def clear(self) -> None:
        self.box.selection_clear(0, tk.END)


class Playlist():

    def __init__(self, double_click: typing.Callable):
        self.list = []              # List of Songs object
        self.active = 0             # Index of active song in self.list
        self.box = PlaylistBox(double_click)    # widget to show songs
        self.INITIAL_DIR = r"/home/jakub/Music" # Pass as argument?
        STARTING_DIR = r"Blackmores Night/Natures Light (2001)" # Pass as argument?
        # Load first songs
        self.add_folder(os.path.join(self.INITIAL_DIR, STARTING_DIR), append=False)

    def get(self) -> Song:
        """ Returns active Song """
        box_active = self.box.get_index()
        if box_active:
            self.active = box_active
        else:
            self.active = 0 # If nothing is selected, start from beginning
        self.box.select(self.active)
        return self.list[self.active]

    def get_next(self) -> Song:
        """ Returns next Song and activates it """
        # 1) Check if an item in box is actively selected
        box_active = self.box.get_index()
        if box_active:
            # 1 True) The index of this selected item is now the active index
            self.active = box_active
        # 1 False) Use active index to select item in box
            
        if self.is_last():   # if active song is last in the playlist, return None
            return None

        # All clear, move to the next song
        self.active += 1
        self.box.select(self.active)
        return self.list[self.active]

    def get_previous(self) -> Song:
        """ Returns previous songs and activates it """
        # 1) Check if an item in box is actively selected
        box_active = self.box.get_index()
        if box_active:
            # 1 True) The index of this selected item is now the active index
            self.active = box_active
        # 1 False) Use active index to select item in box

        if self.is_first():    # If active song is first in playlist, return None
            return None
        
        # All clear, move to the previous song
        self.active -= 1
        self.box.select(self.active)
        return self.list[self.active]

    def is_last(self) -> bool:
        return self.active == len(self.list) - 1

    def is_first(self) -> bool:
        return self.active == 0

    def clear(self) ->  None:
        self.box.clear()
        self.active = 0
        
    # Class method?
    def get_song(self, path: str) -> Song:
        TAG_NAMES = ["artist", "album", "tracknumber", "tracktitle"]
        tags = music_tag.load_file(path)
        # Copy only existing tags
        song = {}
        complete_tags = True
        for tag in TAG_NAMES:
            if tags[tag].value:
                song[tag] = tags[tag].value
            else:   # If tag does not exists, populate with None
                song[tag] = None
                complete_tags = False
        # Add song id
        if complete_tags:
            # All tags found
            filled_tracknumber = str(song['tracknumber']).zfill(2)
            song_id = f"{song['artist']} - {song['album']} - {filled_tracknumber} - {song['tracktitle']}"
        else:
            # At least one tag missing
            full_name = os.path.basename(path)
            song_id = os.path.splitext(full_name)[0]
        song["id"] = song_id
        # Add path
        song["path"] = path
        # Add duration
        file = mutagen.File(path)
        song["duration"] = int(file.info.length) * 1000
        # Return song_id and song
        return Song(song)

    def add_folder(self, path: str, append=True):
        FORMATS = [".mp3", ".vaw", ".ogg"] # Should be saved with mixer and passed to this method
        # Load files
        loaded_files = []
        for root, dirs, files in os.walk(path): # What if path contains subfolders with music files?
            for file in files:
                # Skip non-supported formats
                if os.path.splitext(file)[1] not in FORMATS:
                    continue
                path = os.path.join(root, file)
                loaded_files.append(self.get_song(path))
        # Check if any songs loaded
        if not loaded_files: # TO DO: move to manager
            # No supported songs founds
            self.master.status_bar.set_files_status("No files found")
            self.master.root.after(3000, lambda : self.master.status_bar.set_files_status(""))
            return
        # Delete present songs if not append
        if not append:
            self.list.clear()               # playlist
            self.box.box.delete(0, tk.END)  # playlistbox # TO DO: nadefinovat v PlaylistBox
        # Populate playlistbox with sorted songs
        self.list = loaded_files.copy() # TO DO: sort them
        for song in self.list:
            self.box.box.insert(tk.END, song.id)

    def add_songs(self, paths: list[str]):
        for path in paths:
            loaded_song = self.get_song(path)
            if loaded_song:
                self.list.append(loaded_song)
                self.box.box.insert(tk.END, loaded_song.id)

    def remove_all(self) -> None:
        self.list.clear()
        self.active = 0
