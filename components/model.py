import os

import customtkinter as ctk

from .enums import *
from .mixer.mixer import Mixer
from .mixer.justmixer import JustMixer
from .mixer.pygamemixer import PygameMixer

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


class Model():

    def __init__(self):

        # Controls
        self._mixer: Mixer = JustMixer()
        self.mixer_var = ctk.IntVar(value=2)
        self.formats: list[str] = self.get_supported_formats()
        self._play_state: PlaybackStatus = PlaybackStatus.STOPPED
        self._volume_state: ctk.BooleanVar = ctk.BooleanVar()
        self._volume: float = 1.0 # float or int?
        self.time_var: ctk.IntVar = ctk.IntVar()

        # Playlist
        self.list: list[Song] = {}
        self.active: int = 0 # -1 could mean no selection
        self.STARTING_DIR: str = os.path.join(os.environ["INITIAL_DIR"], os.environ["STARTING_DIR"])


    def set_mixer(self) -> None:
        """Set mixer object"""
        self.stop()
        if self.mixer_var.get() == 1:
            self._mixer = PygameMixer()
        elif self.mixer_var.get() == 2:
            self._mixer = JustMixer()

    def get_supported_formats(self) -> list[str]:
        return self._mixer.supported_formats()
    
    def load_song(self, path: str) -> Song:
        TAG_NAMES: list[str] = ["artist", "album", "tracknumber", "tracktitle"]
        tags = music_tag.load_file(path)
        # Copy only existing tags
        song = {}
        complete_tags: bool = True
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

    def load_songs(self, path: str) -> list[str]:
        loaded_files: list[Song] = []
        for root, dirs, files in os.walk(path):
            for file in files:
                # Skip non-supported formats
                if os.path.splitext(file)[1] not in self.formats:
                    continue
                path = os.path.join(root, file)
                loaded_files.append(self.load_song(path))
        self.list.clear()
        self.list = loaded_files.copy()
        self.list.sort(key=lambda obj: obj.id)
        return [song.id for song in self.list]

    def activate_song(self, id: int) -> None:
        self.active = id

    def get_song(self) -> (Song | None, int):
        """Return active Song"""
        if self.active == -1:
            self.active = 0 # If nothing is selected, start from beginning
        return self.list[self.active], self.active
    
    def _is_last(self) -> bool:
        return self.active == len(self.list) - 1

    def _is_first(self) -> bool:
        return self.active == 0
    
    def get_next(self) -> Song:
        """ Activate the next song in song list and return it """
        if self._is_last():
            return None, -1
        self.active += 1
        return self.list[self.active], self.active
    
    def get_previous(self) -> (Song | None, int):
        """ Activate the previous song in song list and return it """
        if self._is_first():
            return None, -1
        self.active -= 1
        return self.list[self.active], self.active

    def play(self, song: Song) -> PlaybackStatus:
        """Play active song"""
        self._mixer.load(song.path)
        self._mixer.play()
        self._play_state = PlaybackStatus.PLAYING
        return self._play_state

    def pause(self) -> PlaybackStatus | None:
        if self._play_state == PlaybackStatus.PLAYING:
            self._mixer.pause()
            self._play_state = PlaybackStatus.PAUSED
            return PlaybackStatus.PAUSED
        elif self._play_state == PlaybackStatus.PAUSED:
            self._mixer.unpause()
            self._play_state = PlaybackStatus.PLAYING
            return PlaybackStatus.PLAYING
        return None
    
    def stop(self) -> PlaybackStatus:
        self._mixer.stop()
        self._play_state = PlaybackStatus.STOPPED
        self.active = -1
        return self._play_state
    
    def get_duration(self) -> int:
        return int(self._mixer.get_duration())
    
    def set_volume(self, volume: float) -> None:
        self._mixer.set_volume(volume)
        if self._volume_state.get():        # If mute, than...
            self._volume_state.set(False)   # ...unmute

    def mute(self) -> None:
        state: bool = self._volume_state.get()  # True means we are muted
        if state:
            self._mixer.set_volume(self._volume)
            self._volume_state.set(False)
        else:
            self._volume = self._mixer.get_volume()
            self._mixer.set_volume(0.0)
            self._volume_state.set(True)

    def set_time(self, time: int) -> None:
        self._mixer.set_position(time)

    def is_playing_and_not_busy(self) -> bool:
        return (self._play_state == PlaybackStatus.PLAYING) and not self._mixer.get_busy()
    
    ########################################### LOOPS ###########################################
    def loop_runtime(self) -> (PlaybackStatus, int):
        position: int = self._mixer.get_position()
        return self._play_state, position 
