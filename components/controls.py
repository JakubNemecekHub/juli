""" Control Buttons Frame """

import tkinter as tk

from .enums import *
from .mixer.justmixer import JustMixer
from .mixer.pygamemixer import PygameMixer

# Define Protocol for Song? With only what is needed for controls?


class Controls():

    def __init__(self):

        self._mixer = JustMixer()
        self._play_state = PlaybackStatus.STOPPED
        self.volume_state = tk.BooleanVar(False)    # True means is muted
                                                    # Default is False, e.g. umuted
        self._volume = 0                            # Volume level used for unmuting

    def set_mixer(self, mixer: str) -> None:
        """ Set mixer during runtime """
        # Stop everything
        self.stop()
        # Set new mixer
        if mixer == "JustMixer":
            self._mixer = JustMixer()
        elif mixer == "PygameMixer":
            self._mixer = PygameMixer()

    def play(self, song) -> None:
        self._mixer.load(song.path)                 # Load selected song
        self._mixer.play()                          # Play the song
        self._play_state = PlaybackStatus.PLAYING   # Set status

    def pause(self) -> bool:
        if self._play_state == PlaybackStatus.PLAYING:
            self._mixer.pause()
            self._play_state = PlaybackStatus.PAUSED
            return PlaybackStatus.PAUSED
        elif self._play_state == PlaybackStatus.PAUSED:
            self._mixer.unpause()
            self._play_state = PlaybackStatus.PLAYING
            return PlaybackStatus.PLAYING
        return None

    def stop(self) -> bool:
        self._mixer.stop()
        self._play_state = PlaybackStatus.STOPPED
        return True

    def is_playing(self) -> bool:
        return self._play_state == PlaybackStatus.PLAYING

    def is_paused(self) -> bool:
        return self._play_state == PlaybackStatus.PAUSED

    def is_stopped(self) -> bool:
        return self._play_state == PlaybackStatus.STOPPED

    def is_busy_not_playing(self) -> None:
        return self.is_playing() and not self._mixer.get_busy()

    def get_volume(self) -> float:
        return self._mixer.get_volume()

    def set_volume(self, volume: float) -> None:
        self._mixer.set_volume(volume)
        if self.volume_state.get():
            self.volume_state.set(False)

    def toggle_mute(self) -> None:
        if self.volume_state.get():     # Activate mute
            self._volume = self._mixer.get_volume()
            self._mixer.set_volume(0.0)
            self.volume_state.set(True)
        else:                           # Deactivate mute
            self._mixer.set_volume(self._volume)
            self.volume_state.set(False)

    def get_position(self) -> int:
        return self._mixer.get_position()

    def set_position(self, position: int) -> None:
        self._mixer.set_position(position)
        # duration = self.master.mixer.get_duration()
        # value = duration * (int(position) / 100)

    def get_duration(self) -> int:
        return int(self._mixer.get_duration())

    def supported_formats(self) -> list[str]:
        return self._mixer.supported_formats()

    def file_types(self) -> list[str]:
        return self._mixer.file_types()
