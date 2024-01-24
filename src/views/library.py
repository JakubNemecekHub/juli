"""
Contents of the Library tab.
Allows song loading an mixer selection.
"""

from typing import Protocol

import customtkinter as ctk

from src.enums import MixerEnum


class Controller(Protocol):
    """ Interface for the Controller object. """
    def load_songs(self, path: str) -> None:
        ...
    def set_mixer(self, mixer: MixerEnum) -> None:
        ...


class FolderFrame(ctk.CTkFrame):
    """ Song loading. """
    def __init__(self, root: ctk.CTkFrame, ctr: Controller) -> None:
        super().__init__(root)
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        self.folder_entry_label: ctk.CTkLabel = ctk.CTkLabel(self, text="Enter path")
        self.folder_entry_label.grid(row=0, column=0, sticky="ew")
        self.folder_entry: ctk.CTkEntry = ctk.CTkEntry(self, placeholder_text="Path...")
        self.folder_entry.grid(row=0, column=1, columnspan=2, sticky="ew", pady=(0, 12))
        self.btn_load: ctk.CTkButton = ctk.CTkButton(self, text="Load Songs")
        self.btn_load.grid(row=1, column=1)
        self.btn_load.configure(command=lambda: ctr.load_songs(self.folder_entry.get()))
        self.btn_add: ctk.CTkButton = ctk.CTkButton(self, text="Add Songs")
        self.btn_add.grid(row=1, column=2)


class MixerFrame(ctk.CTkFrame):
    """ Mixer selection. """
    def __init__(self, root: ctk.CTkFrame, ctr: Controller) -> None:
        super().__init__(root)
        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.lb_mixer: ctk.CTkLabel = ctk.CTkLabel(self, text="Mixer")
        self.lb_mixer.grid(row=0, column=0)
        self.mixer_var: ctk.IntVar = ctk.IntVar(value=MixerEnum.JUST_PLAYBACK.value)
        self.ra_mixer_pygame: ctk.CTkRadioButton = ctk.CTkRadioButton(self, text="Pygame Mixer", value=MixerEnum.PYGAME.value, variable=self.mixer_var)
        self.ra_mixer_justmixer: ctk.CTkRadioButton = ctk.CTkRadioButton(self, text="JustMixer", value=MixerEnum.JUST_PLAYBACK.value, variable=self.mixer_var)
        self.ra_mixer_pygame.grid(row=0, column=1)
        self.ra_mixer_justmixer.grid(row=0, column=2)
        self.ra_mixer_justmixer.configure(command=ctr.set_mixer)
        self.ra_mixer_justmixer.configure(command=lambda: ctr.set_mixer(MixerEnum(self.mixer_var.get())))
        self.ra_mixer_pygame.configure(command=lambda: ctr.set_mixer(MixerEnum(self.mixer_var.get())))
