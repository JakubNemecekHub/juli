import os
import customtkinter as ctk
from tkinter import filedialog
from PIL import Image

from .controls import Controls
from .playlist import Playlist
from .statusbar import StatusBar
from .playbar import PlayBar
from .menu import Menu
from .enums import *


class Manager():

    def __init__(self, root: ctk.CTk):

        self.time_var = ctk.IntVar()

        self.controls = Controls()                         # Controls # WIP
        self.play_bar = PlayBar(root)                      # Play Bar # WIP
        self.playlist = Playlist(root, self.double_click)  # Playlist # WIP
        self.formats = self.controls.supported_formats()
        self.INITIAL_DIR = os.environ["INITIAL_DIR"]
        # Load first songs
        dir = os.path.join(self.INITIAL_DIR, os.environ["STARTING_DIR"])
        self.playlist.add_folder(dir, self.formats, append=False)
        self.status_bar = StatusBar(root)                  # Status Bar # WIP

        self.gui = ManagerGui(
            root,
            self.play,
            self.pause,
            self.stop,
            self.previous,
            self.next,
            self.controls.get_volume(),
            self.set_volume,
            self.controls.volume_state,
            self.mute,
            self.time_var,
            self.set_position
        )

        self.menu = Menu(
            root,
            self.menu_open_folder,
            self.menu_add_folder,
            self.menu_add_songs,
            self.mixer_set_justplayback,
            self.mixer_set_pygame
        )

        # TO DO: Sort pack order in manager
        self.play_bar.frame.pack(fill=ctk.X)
        self.gui.frame.pack(fill=ctk.X)
        self.playlist.frame.pack(fill=ctk.X)
        self.status_bar.frame.pack(fill=ctk.X)

    # === Menu
    # === ==== Files
    def menu_open_folder(self) -> None:
        dir = filedialog.askdirectory(initialdir=self.INITIAL_DIR, title="Select a folder")
        if dir:
            # Directory selected
            self.controls.stop()
            if not self.playlist.add_folder(dir, self.formats, append=False):
                # No supported files found
                self.status_bar.set_message("No files found")

    def menu_add_folder(self) -> None:
        dir = filedialog.askdirectory(initialdir=self.INITIAL_DIR, title="Select a folder")
        if dir:
            # Directory selected
            self.controls.stop()
            if not self.playlist.add_folder(dir, self.formats, append=True):
                # No supported files found
                self.status_bar.set_message("No files found")

    def menu_add_songs(self) -> None:
        types = self.controls.file_types()
        selection = filedialog.askopenfilenames(initialdir=self.INITIAL_DIR, title="Select a song", filetypes=types)
        self.playlist.add_songs(selection)
    # === ==== Mixers
    def mixer_set_justplayback(self) -> None:
        self.controls.set_mixer("JustMixer")

    def mixer_set_pygame(self) -> None:
        self.controls.set_mixer("PygameMixer")

    # === Playback
    def play(self) -> None:
        # 1) Get song from Playlist
        current_song = self.playlist.get()
        # 2) Play the song
        if current_song:
            self.controls.play(current_song)
            # 3) Update play bar
            self.play_bar.set(current_song)
            # 4) Update status bar
            self.status_bar.set_status(PlaybackStatus.PLAYING.value)
            # 5) Update time scale range
            self.gui.scl_time.configure(to=self.controls.get_duration())

    def pause(self) -> None:
        pause_results = self.controls.pause()
        if pause_results:
            self.status_bar.set_status(pause_results.value)

    def stop(self) -> None:
        if self.controls.stop():
            self.playlist.clear()
            # Update play bar
            self.play_bar.reset_song()
            # Update status bar
            self.status_bar.set_status(PlaybackStatus.STOPPED.value)

    def previous(self) -> None:
        previous_song = self.playlist.get_previous()    # 1) Get previous song from Playlist
        if previous_song:                               # 2) If such a song exists, play it
            self.controls.play(previous_song)
            self.play_bar.set(previous_song)            # 3) Update play bar
            self.status_bar.set_status(PlaybackStatus.PLAYING.value)    # 4) Update status bar

    def next(self) -> None:
        next_song = self.playlist.get_next()    # 1) Get next song from Playlist
        if next_song:                           # 2) If such a song exists, play it
            self.controls.play(next_song)       
            self.play_bar.set(next_song)        # 3) Update play bar
            self.status_bar.set_status(PlaybackStatus.PLAYING.value)    # 4) Update status bar

    def set_volume(self, volume: float) -> None:
        self.controls.set_volume(volume)

    def mute(self) -> None:
        self.controls.toggle_mute()

    def double_click(self, song_id: str) -> None:
        self.play()

    def continue_playback(self) -> None:
        if self.controls.is_busy_not_playing():
            # If at the last song of the playlist -> STOPPED
            if self.playlist.is_last():
                self.stop()
            else:
                # Player is playing but the mixer is not busy
                # Not at the last song in playlist
                # -> play next song
                self.next()

        self.play_bar.frame.after(100, self.continue_playback)

    def loop_runtime(self) -> None:
        if self.controls.is_playing():
            duration = self.controls.get_duration()
            position = self.controls.get_position()
            # Update time label
            self.play_bar.set_time(position)
            # Update time scale
            self.time_var.set(position)
        elif self.controls.is_stopped():
            self.play_bar.reset_time()  # Reset time label
            self.gui.reset_position()   # Reset time scale

        self.play_bar.frame.after(100, self.loop_runtime)

    def set_position(self, time: str) -> None:
        self.controls.set_position(int(time))


class ManagerGui():

    def __init__(self, root: ctk.CTk, play, pause, stop, previous, next, volume, set_volume, mute_var, mute_com, time_var, set_position):

        # Load icons
        # Must be self... otherwise Python garbage collector will destroy them
        # Is there any other way?
        _icon_folder = "icons"
        self.icon_play = ctk.CTkImage(Image.open(os.path.join(_icon_folder, "controls", "play.png")))
        self.icon_pause = ctk.CTkImage(Image.open(os.path.join(_icon_folder, "controls", "pause.png")))
        self.icon_stop = ctk.CTkImage(Image.open(os.path.join(_icon_folder, "controls", "stop.png")))
        self.icon_previous = ctk.CTkImage(Image.open(os.path.join(_icon_folder, "controls", "previous.png")))
        self.icon_next = ctk.CTkImage(Image.open(os.path.join(_icon_folder, "controls", "next.png")))

        self.frame = ctk.CTkFrame(root)
        # Play
        btn_play = ctk.CTkButton(self.frame, image=self.icon_play, text="", border_width=0, command=play, width=22)
        btn_play.grid(row=0, column=0, padx=7, pady=2.5)
        # Pause
        btn_pause = ctk.CTkButton(self.frame, image=self.icon_pause, text="", border_width=0, command=pause, width=22)
        btn_pause.grid(row=0, column=1, padx=7, pady=2.5)
        # Stop
        btn_stop = ctk.CTkButton(self.frame, image=self.icon_stop, text="", border_width=0, command=stop, width=22)
        btn_stop.grid(row=0, column=2, padx=7, pady=2.5)
        # Previous
        btn_previous = ctk.CTkButton(self.frame, image=self.icon_previous, text="", border_width=0, command=previous, width=22)
        btn_previous.grid(row=0, column=3, padx=7, pady=2.5)
        # Next
        btn_next = ctk.CTkButton(self.frame, image=self.icon_next, text="", border_width=0, command=next, width=22)
        btn_next.grid(row=0, column=4, padx=7, pady=2.5)

        # Volume
        # Volume Scale
        scl_volume = ctk.CTkSlider(self.frame, command=set_volume, orientation=ctk.HORIZONTAL)
        scl_volume.set(volume * 100)
        scl_volume.grid(row=1, column=0, columnspan=8, pady=12)
        # Mute
        chbtn_mute = ctk.CTkSwitch(self.frame, text="Mute", variable=mute_var, command=mute_com)
        chbtn_mute.grid(row=1, column=9, pady=12)

        # Time
        self.scl_time = ctk.CTkSlider(self.frame, from_=0, to=100, variable=time_var, command=set_position, orientation=ctk.HORIZONTAL, width=360)
        self.scl_time.grid(row=2, column=1, columnspan=9, pady=12)
        self.scl_time.set(0)

    def update_position(self, time: int) -> None:
        self.scl_time.set(time)

    def reset_position(self) -> None:
        self.scl_time.set(0)

    # def song_set_position(self, time) -> None:
    #     # I need to be able to tell if scale was moved automatically or by user
    #     # ->
    #     print("second")
