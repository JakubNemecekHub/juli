import os
from enum import Enum
import tkinter as tk

# from components.mixer.pygamemixer import PygameMixer as Mixer
from components.mixer.justmixer import JustMixer as Mixer
from components.volume import VolumeControls
from components.track import TrackFrame
from components.controls import Controls
from components.playlist import Playlist
from components.menu import Menu
from components.statusbar import StatusBar


class PlaybackStatus(Enum):
    STOPPED = "Stopped"
    PLAYING = "Playing"
    PAUSED = "Paused"


class MusicPlayer():

    def __init__(self):
        self.root = tk.Tk()    # The TkInter window object
        self.root.title("Juli Music Player")
        self.root.iconphoto(False, tk.PhotoImage(file = "icon.png"))
        self.root.geometry("1000x300+100+100") # Height x Width + x + y positions
        self.mixer = Mixer()
        # Constants
        self.INITIAL_DIR = r"/home/jakub/Music"
        self.status_enum = PlaybackStatus
        # Get default volume
        self.volume = self.mixer.get_volume()

        # Flags
        self.playback_status = self.status_enum.STOPPED

        self.status_bar = StatusBar(self)           # Status Bar
        self.track = TrackFrame(self)               # Track Frame
        self.playlist = Playlist(self)              # Playlist
        self.controls = Controls(self)              # Controls
        self.menu = Menu(self)                      # Menu
        self.frame_volume = VolumeControls(self)    # Volume Controls


if __name__ == "__main__":
    player = MusicPlayer()
    player.track.loop_runtime()
    player.playlist.loop_continuity()
    player.root.mainloop()
