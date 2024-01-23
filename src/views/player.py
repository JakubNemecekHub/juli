import os
import time

import customtkinter as ctk
import CTkListbox as ctkl
from PIL import Image

from ..model import Song


class ControlFrame(ctk.CTkFrame):

    def __init__(self, root, ctr):
        super().__init__(root)
        # GUI
        _icon_folder = os.path.join("icons", "controls")
        self.play = ctk.CTkImage(Image.open(os.path.join(_icon_folder, "play.png")))
        self.pause = ctk.CTkImage(Image.open(os.path.join(_icon_folder, "pause.png")))
        self.stop = ctk.CTkImage(Image.open(os.path.join(_icon_folder, "stop.png")))
        self.previous = ctk.CTkImage(Image.open(os.path.join(_icon_folder, "previous.png")))
        self.next = ctk.CTkImage(Image.open(os.path.join(_icon_folder, "next.png")))

        def create_button(root, icon, row, column, command) -> ctk.CTkButton:
            btn = ctk.CTkButton(root, image=icon, text="", command=command)
            btn.grid(row=row, column=column, sticky="ew", padx=2, pady=(4,12))
            return btn
        
        self.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.btn_play = create_button(self, self.play, 0, 0, ctr.play)              # Play
        self.btn_pause = create_button(self, self.pause, 0, 1, ctr.pause)           # Pause
        self.btn_stop = create_button(self, self.stop, 0, 2, ctr.stop)              # Stop
        self.btn_previous = create_button(self, self.previous, 0, 3, ctr.previous)  # Previous
        self.btn_next = create_button(self, self.next, 0, 4, ctr.next)              # Next


class VolumeFrame(ctk.CTkFrame):

    def __init__(self, root, ctr):
        super().__init__(root)
        self.grid_columnconfigure(0, weight=5)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        # Volume Scale
        self.scl_volume = ctk.CTkSlider(self, orientation=ctk.HORIZONTAL, command=ctr.set_volume)
        self.scl_volume.set(1)
        self.scl_volume.grid(row=0, column=0, pady=(0,12))
        # Mute
        self.chbtn_mute = ctk.CTkSwitch(self, text="Mute", command=ctr.mute)
        self.chbtn_mute.grid(row=0, column=1, pady=(0,12))


class InfoFrame(ctk.CTkFrame):

    def __init__(self, root, ctr):
        super().__init__(root)
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure((1, 2), weight=1)
        self.grid_rowconfigure((0, 1), weight=1)
        # Time
        self.scl_time = ctk.CTkSlider(self, from_=0, to=100, orientation=ctk.HORIZONTAL, width=360, command=ctr.set_time)
        self.scl_time.grid(row=0, column=0, columnspan=3, sticky="ew")
        self.scl_time.set(0)
        self.time_var: ctk.StringVar = ctk.StringVar()
        self.duration_var: ctk.StringVar = ctk.StringVar()
        l_time = ctk.CTkLabel(self, textvariable=self.time_var, anchor="e")
        l_time.grid(row=1, column=1, sticky="ew")
        l_duration = ctk.CTkLabel(self, textvariable=self.duration_var, anchor="e")
        l_duration.grid(row=1, column=2, sticky="ew")
        # Play Bar
        self.track_var: ctk.StringVar = ctk.StringVar()
        l_track = ctk.CTkLabel(self, textvariable=self.track_var, anchor="w")
        l_track.grid(row=1, column=0, sticky="ew")

    def time_str(self, ms: int) -> str:
        """ Converts input milliseconds into formated time string """
        _format = "%M:%S"  # Show hours only when necessary
        if ms >= 3600000:
            _format = "%H:%M:%S"
        return time.strftime(_format, time.gmtime(ms // 1000))     

    def update(self, song: Song) -> None:
        self.track_var.set(song.tracktitle)
        if song.duration:
            self.duration_var.set(self.time_str(song.duration))
            self.scl_time.configure(to=song.duration)

    def time(self, time: int) -> None:
        self.time_var.set(self.time_str(time))
        self.scl_time.set(time)

    def reset(self) -> None:
        self.track_var.set("")
        self.duration_var.set("")
        self.time_var.set("")
        self.scl_time.set(0)


class PlayListFrame(ctk.CTkFrame):
        
    def __init__(self, root, ctr):
        super().__init__(root)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.playlist = ctkl.CTkListbox(self, command=ctr.click)
        self.playlist.bind("<Double-1>", ctr.double_click)
        self.playlist.grid(row=0, column=0, sticky="nsew")

    def populate(self, songs: list[str]) -> None:
        self.playlist.delete("all")
        for song in songs:
            self.playlist.insert(ctk.END, song)

    def update(self, id: int) -> None:
        self.playlist.activate(id)

    def deselect(self, id: int) -> None:
        self.playlist.deactivate(id)

    def get(self) -> (tuple | int | None):
        return self.playlist.curselection()