import os
import tkinter as tk
from tkinter import filedialog

from .controls import Controls
from .playlist import Playlist
from .statusbar import StatusBar
from .playbar import PlayBar
from .menu import Menu
from .enums import *

class Manager():

    def __init__(self, root: tk.Tk):

        self.time_var = tk.IntVar()
       
        self.controls = Controls()      # Controls # WIP
        self.play_bar = PlayBar()       # Play Bar # WIP
        self.playlist = Playlist(self.double_click)      # Playlist # WIP
        self.status_bar = StatusBar()   # Status Bar # WIP

        self.gui = ManagerGui(
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
            self.menu_add_songs
        )

        # TO DO: Sort pack order in manager
        self.play_bar.frame.pack(fill=tk.X)
        self.gui.frame.pack(fill=tk.X)
        self.playlist.box.frame.pack(fill=tk.X)
        self.status_bar.frame.pack(fill=tk.X)

    # === Menu
    def menu_open_folder(self) -> None:
        dir = filedialog.askdirectory(initialdir=self.playlist.INITIAL_DIR, title="Select a folder")
        if dir:
            # Directory selected
            self.controls.stop()
            if not self.playlist.add_folder(dir, append=False):
                # No supported files found
                self.status_bar.set_message("No files found")

    def menu_add_folder(self) -> None:
        dir = filedialog.askdirectory(initialdir=self.playlist.INITIAL_DIR, title="Select a folder")
        if dir:
            # Directory selected
            self.controls.stop()
            if not self.playlist.add_folder(dir, append=True):
                # No supported files found
                self.status_bar.set_message("No files found")

    def menu_add_songs(self) -> None:
        FILE_TYPES = [("Music format", ".mp3"), ("Music format", ".vaw"), ("Music format", ".ogg")] # Must be based on Mixer capabilities
        selection = filedialog.askopenfilenames(initialdir=self.playlist.INITIAL_DIR, title="Select a song", filetypes=FILE_TYPES)
        self.playlist.add_songs(selection)

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
            self.gui.scl_time.config(to=self.controls.get_duration())
    
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
        # 1) Get previous song from Playlist
        previous_song = self.playlist.get_previous()
        # 2) If such a song exists, play it
        if previous_song:
            self.controls.play(previous_song)
            # 3) Update play bar
            self.play_bar.set(previous_song)
            # 4) Update status bar
            self.status_bar.set_status(PlaybackStatus.PLAYING.value)

    def next(self) -> None:
        # 1) Get next song from Playlist
        next_song = self.playlist.get_next()
        # 2) If such a song exists, play it
        if next_song:
            self.controls.play(next_song)
            # 3) Update play bar
            self.play_bar.set(next_song)
            # 4) Update status bar
            self.status_bar.set_status(PlaybackStatus.PLAYING.value)

    def set_volume(self, volume: str) -> None:
        _volume = int(volume)/100
        self.controls.set_volume(_volume)

    def mute(self) -> None:
        self.controls.toggle_mute()

    def double_click(self, event: tk.Event) -> None:
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

    def __init__(self, play, pause, stop, previous, next, volume, set_volume, mute_var, mute_com, time_var, set_position):

        # Load icons
        # Must be self... otherwise Python garbage collector will destroy them
        # Is there any other way?
        _icon_folder = "icons"
        self.icon_play = tk.PhotoImage(file=os.path.join(_icon_folder, "play.png")).subsample(2, 2)
        self.icon_pause = tk.PhotoImage(file=os.path.join(_icon_folder, "pause.png")).subsample(2, 2)
        self.icon_stop = tk.PhotoImage(file=os.path.join(_icon_folder, "stop.png")).subsample(2, 2)
        self.icon_previous = tk.PhotoImage(file=os.path.join(_icon_folder, "previous.png")).subsample(2, 2)
        self.icon_next = tk.PhotoImage(file=os.path.join(_icon_folder, "next.png")).subsample(2, 2)

        self.frame = tk.LabelFrame(relief=tk.FLAT) 
        # frame.pack(fill=tk.X)
        # Play
        btn_play = tk.Button(self.frame, image=self.icon_play, borderwidth=0, command=play)
        btn_play.grid(row=0, column=0, padx=7, pady=2.5)
        # Pause
        btn_pause = tk.Button(self.frame, image=self.icon_pause, borderwidth=0, command=pause)
        btn_pause.grid(row=0, column=1, padx=7, pady=2.5)
        # Stop
        btn_stop = tk.Button(self.frame, image=self.icon_stop, borderwidth=0, command=stop)
        btn_stop.grid(row=0, column=2, padx=7, pady=2.5)
        # Previous
        btn_previous = tk.Button(self.frame, image=self.icon_previous, borderwidth=0, command=previous)
        btn_previous.grid(row=0, column=3, padx=7, pady=2.5)
        # Next
        btn_next = tk.Button(self.frame, image=self.icon_next, borderwidth=0, command=next)
        btn_next.grid(row=0, column=4, padx=7, pady=2.5)
        # Volume
        # Volume Scale
        scl_volume = tk.Scale(self.frame, showvalue=0, command=set_volume, orient=tk.HORIZONTAL)
        scl_volume.set(volume * 100)
        scl_volume.grid(row=0, column=5, columnspan=3)
        # Mute
        chbtn_mute = tk.Checkbutton(self.frame, text="Mute", variable=mute_var, command=mute_com)
        chbtn_mute.grid(row=0, column=9)
        # Time
        self.scl_time = tk.Scale(self.frame, showvalue=0,from_=0, to=100, variable=time_var, command=set_position, orient=tk.HORIZONTAL, length=360)
        self.scl_time.grid(row=1, column=0, columnspan=10)
        self.scl_time.set(0)

    def update_position(self, time: int) -> None:
        self.scl_time.set(time)

    def reset_position(self) -> None:
        self.scl_time.set(0)

    # def song_set_position(self, time) -> None:
    #     # I need to be able to tell if scale was moved automatically or by user
    #     # ->
    #     print("second")
