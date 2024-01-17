import os

import customtkinter as ctk
import CTkListbox as ctkl
from PIL import Image
import time
from typing import Callable

from .model import Song


class ButtonIcons():

    def __init__(self):
        _icon_folder = os.path.join("icons", "controls")
        self.play = ctk.CTkImage(Image.open(os.path.join(_icon_folder, "play.png")))
        self.pause = ctk.CTkImage(Image.open(os.path.join(_icon_folder, "pause.png")))
        self.stop = ctk.CTkImage(Image.open(os.path.join(_icon_folder, "stop.png")))
        self.previous = ctk.CTkImage(Image.open(os.path.join(_icon_folder, "previous.png")))
        self.next = ctk.CTkImage(Image.open(os.path.join(_icon_folder, "next.png")))


class View():

    def __init__(self, root):

        # Create tabs for music player and library management 
        self.manager_tab_view = ctk.CTkTabview(root)
        tab_player = self.manager_tab_view.add("Player")
        tab_library = self.manager_tab_view.add("Library")
        self.manager_tab_view.set("Player")
        root.grid_columnconfigure(0, weight=1)
        root.grid_rowconfigure(0, weight=1)
        self.manager_tab_view.grid(row=0, column=0, sticky="nsew")

        ########################################### POPULATE PLAYER TAB ###########################################

        # Load icons
        self.icons = ButtonIcons()
        
        tab_player.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
        tab_player.grid_rowconfigure((0, 1, 2, 3, 5), weight=1)
        # Controls
        # Play
        self.btn_play = ctk.CTkButton(tab_player, image=self.icons.play, text="")
        self.btn_play.grid(row=0, column=0, sticky="ew", padx=2, pady=(4, 12))
        # Pause
        self.btn_pause = ctk.CTkButton(tab_player, image=self.icons.pause, text="")
        self.btn_pause.grid(row=0, column=1, sticky="ew", padx=2, pady=(4, 12))
        # Stop
        self.btn_stop = ctk.CTkButton(tab_player, image=self.icons.stop, text="")
        self.btn_stop.grid(row=0, column=2, sticky="ew", padx=2, pady=(4, 12))
        # Previous
        self.btn_previous = ctk.CTkButton(tab_player, image=self.icons.previous, text="")
        self.btn_previous.grid(row=0, column=3, sticky="ew", padx=2, pady=(4, 12))
        # Next
        self.btn_next = ctk.CTkButton(tab_player, image=self.icons.next, text="")
        self.btn_next.grid(row=0, column=4, sticky="ew", padx=2, pady=(4, 12))

        # Volume
        # Volume Scale
        self.scl_volume = ctk.CTkSlider(tab_player, orientation=ctk.HORIZONTAL, )
        self.scl_volume.set(1)
        self.scl_volume.grid(row=1, column=0, columnspan=3, pady=(0,12))
        # Mute
        self.chbtn_mute = ctk.CTkSwitch(tab_player, text="Mute")
        self.chbtn_mute.grid(row=1, column=3, columnspan=2, pady=(0,12))

        # Time
        self.scl_time = ctk.CTkSlider(tab_player, from_=0, to=100, orientation=ctk.HORIZONTAL, width=360)
        self.scl_time.grid(row=2, column=0, columnspan=5, sticky="ew")
        self.scl_time.set(0)

        # Play Bar
        self._track: ctk.StringVar = ctk.StringVar()
        self._time: ctk.StringVar = ctk.StringVar()
        self._duration: ctk.StringVar = ctk.StringVar()
        l_track = ctk.CTkLabel(tab_player, textvariable=self._track, anchor="w")
        l_track.grid(row=3, column=0, columnspan=3, sticky="ew")
        l_time = ctk.CTkLabel(tab_player, textvariable=self._time, anchor="e")
        l_time.grid(row=3, column=3, sticky="ew")
        l_duration = ctk.CTkLabel(tab_player, textvariable=self._duration, anchor="e")
        l_duration.grid(row=3, column=4, sticky="ew")
        
        # Playlist
        tab_player.grid_rowconfigure(4, weight=20)
        self.playlist = ctkl.CTkListbox(tab_player)
        self.playlist.grid(row=4, column=0, columnspan=5, sticky="nsew")

        # Status Bar
        self._status: ctk.StringVar = ctk.StringVar()
        self._message: ctk.StringVar = ctk.StringVar()
        l_status = ctk.CTkLabel(tab_player, textvariable=self._status, anchor="w")
        l_status.grid(row=5, column=0, columnspan=2, sticky="ew")
        # Message label
        l_message = ctk.CTkLabel(tab_player, textvariable=self._message, anchor="w")
        l_message.grid(row=5, column=2, columnspan=3, sticky="ew") 

        ########################################### POPULATE LIBRARY TAB ###########################################

        tab_library.grid_columnconfigure((0, 1, 2), weight=1)
        tab_library.grid_rowconfigure((0, 1, 2), weight=1)
        tab_library.grid_rowconfigure(3, weight=10)

        folder_entry_label: ctk.CTkLabel = ctk.CTkLabel(tab_library, text="Enter path")
        folder_entry_label.grid(row=0, column=0, sticky="ew")
        self.folder_entry: ctk.CTkEntry = ctk.CTkEntry(tab_library, placeholder_text="Path...")
        self.folder_entry.grid(row=0, column=1, columnspan=2, sticky="ew")
        self.btn_load: ctk.CTkButton = ctk.CTkButton(tab_library, text="Load Songs")
        self.btn_load.grid(row=1, column=1)
        self.btn_add: ctk.CTkButton = ctk.CTkButton(tab_library, text="Add Songs")
        self.btn_add.grid(row=1, column=2)

        # Mixer selection -> radiobuttons (for more -> drop down list)
        lb_mixer: ctk.CTkLabel = ctk.CTkLabel(tab_library, text="Mixer")
        lb_mixer.grid(row=2, column=0)
        self.ra_mixer_pygame: ctk.CTkRadioButton = ctk.CTkRadioButton(tab_library, text="Pygame Mixer", value=1)
        self.ra_mixer_justmixer: ctk.CTkRadioButton = ctk.CTkRadioButton(tab_library, text="JustMixer", value=2)
        self.ra_mixer_pygame.grid(row=2, column=1)
        self.ra_mixer_justmixer.grid(row=2, column=2)

    ########################################### BIND VARIOUS COMMANDS ###########################################

    def bind_commands(self, play, pause, stop, previous, next) -> None:
        self.btn_play.configure(command=play)
        self.btn_pause.configure(command=pause)
        self.btn_stop.configure(command=stop)
        self.btn_previous.configure(command=previous)
        self.btn_next.configure(command=next)

    def bind_volume(self, command) -> None:
        self.scl_volume.configure(command=command)

    def bind_mute(self, command) -> None:
        self.chbtn_mute.configure(command=command)

    def bind_time(self, command) -> None:
        self.scl_time.configure(command=command)

    def bind_load(self, command) -> None:
        self.btn_load.configure(command=lambda: command(self.folder_entry.get()))

    def bind_playlist(self, click: Callable, double_click: Callable) -> None:
        self.playlist.configure(command=click)
        self.playlist.bind("<Double-1>", double_click)

    def bind_time(self, command: Callable) -> None:
        self.scl_time.configure(command=command)

    def bind_mixer_selection(self, command: Callable, var: ctk.IntVar) -> None:
        self.ra_mixer_justmixer.configure(command=command, variable=var)
        self.ra_mixer_pygame.configure(command=command, variable=var)

    ########################################### UTILS ###########################################

    def time_str(self, ms: int) -> str:
        """ Converts input milliseconds into formated time string """

        # Show hours only when necessary
        _format = "%M:%S"
        if ms >= 3600000:
            _format = "%H:%M:%S"

        return time.strftime(_format, time.gmtime(ms // 1000)) 

    ########################################### INTERFACE ###########################################

    def populate_list(self, songs: list[str]) -> None:
        self.playlist.delete("all")
        for song in songs:
            self.playlist.insert(ctk.END, song)

    def update_play_bar(self, song: Song) -> None:
        self._track.set(song.tracktitle)
        if song.duration:
            self._duration.set(self.time_str(song.duration))

    def reset_play_bar(self) -> None:
        self._track.set("")
        self._duration.set("")

    def update_play_list(self, id: int) -> None:
        self.playlist.activate(id)

    def playlist_deselect(self, id: int) -> None:
        self.playlist.deactivate(id)
        pass

    def update_status_bar(self, status: str) -> None:
        self._status.set(status)

    def set_message(self, message: str) -> None:
        self._message.set(message)
        self.tab_player.after(3000, self.reset_message)

    def reset_message(self) -> None:
        self._message.set("")

    def set_time_range(self, duration: int) -> None:
        self.scl_time.configure(to=duration)

    def set_time(self, time: int) -> None:
        self._time.set(self.time_str(time))
        self.scl_time.set(time)

    def reset_time(self) -> None:
        self._time.set("")
        self.scl_time.set(0)

    def get_selection(self) -> None:
        return self.playlist.curselection()
