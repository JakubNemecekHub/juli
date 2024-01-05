import os
import customtkinter as ctk
import CTkListbox as ctkl
import typing

import music_tag
import mutagen


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


class Playlist():

    def __init__(self, root: ctk.CTk, double_click: typing.Callable):
        self.list: list[Song] = {}        # List of Songs object
        self.active: int = ""             # Index of active song in self.list
        # GUI
        self.frame = ctk.CTkFrame(root)
        self.box = ctkl.CTkListbox(self.frame, command=self.click, height=24)
        self.box.pack(fill=ctk.BOTH)
        # Set up left mouse double click
        self.box.bind("<Double-1>", double_click)

    def click(self, index: int) -> None:
        self.active = self.box.curselection()

    def get(self) -> Song:
        """ Returns active Song """
        box_active = self.box.curselection()
        if box_active:
            self.active = box_active
        else:
            self.active = 0 # If nothing is selected, start from beginning
        self.box.activate(self.active)
        return self.list[self.active]

    def get_next(self) -> Song:
        """ Activate the next song in song list and return it """
        if self.is_last():
            return None
        self.active = self.active + 1
        self.box.activate(self.active)
        return self.list[self.active]

    def get_previous(self) -> Song:
        """ Activate the previous song in song list and return it """
        if self.is_first():
            return None
        self.active = self.active - 1
        self.box.activate(self.active)
        return self.list[self.active]

    def is_last(self) -> bool:
        return self.active == len(self.list) - 1

    def is_first(self) -> bool:
        return self.active == 0

    def clear(self) ->  None:
        self.box.deactivate(self.active)
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
            song_id = os.path.splitext(full_name)[0]    # Create id from filename
            song["tracktitle"] = song_id                # Create tracktitle from filename
        song["id"] = song_id
        # Add path
        song["path"] = path
        # Add duration
        file = mutagen.File(path)
        song["duration"] = int(file.info.length) * 1000
        # Return song_id and song
        return Song(song)

    def add_folder(self, path: str, formats: list[str], append=True) -> bool:
        # Load files
        loaded_files: list[Song] = []
        for root, dirs, files in os.walk(path): # What if path contains subfolders with music files?
            for file in files:
                # Skip non-supported formats
                if os.path.splitext(file)[1] not in formats:
                    continue
                path = os.path.join(root, file)
                loaded_files.append(self.get_song(path))
        # Check if any songs loaded
        if not loaded_files:
            # No supported songs founds
            return False
        # Delete present songs if not append
        if not append:
            self.list.clear()               # playlist
            # self.box.box.delete(0, ctk.END)  # playlistbox # TO DO: nadefinovat v PlaylistBox
        # Populate playlistbox with songs
        self.list = loaded_files.copy()
        self.list.sort(key=lambda obj: obj.id) # Sort them by their id
        for song in self.list:
            self.box.insert(ctk.END, song.id)
        return True

    def add_songs(self, paths: list[str]):
        for path in paths:
            loaded_song = self.get_song(path)
            if loaded_song:
                self.list.append(loaded_song)
                self.box.insert(ctk.END, loaded_song.id)

    def remove_all(self) -> None:
        self.list.clear()
        self.active = 0
