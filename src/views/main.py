"""
Main GUI frame.
Holds tabs for player and library, and status frame at the bottom.
"""

import customtkinter as ctk

from src.enums import PlaybackStatus

class StatusFrame(ctk.CTkFrame):
    """ Frame showing playback status and one message. """
    def __init__(self, root: ctk.CTkFrame) -> None:
        super().__init__(root)
        # Logic
        self.MESSAGE_TIME: int = 3000
        self.status_var: ctk.StringVar = ctk.StringVar()
        self.message_var: ctk.StringVar = ctk.StringVar()
        # GUI
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)
        # Status label
        status = ctk.CTkLabel(self, textvariable=self.status_var, anchor="w")
        status.grid(row=0, column=0, sticky="ew")
        # Message label
        message = ctk.CTkLabel(self, textvariable=self.message_var, anchor="w")
        message.grid(row=0, column=1, sticky="ew")

    def status(self, status: PlaybackStatus) -> None:
        """ Set status message. """
        self.status_var.set(status.value)

    def message(self, message: str) -> None:
        """ Set message. Will appear only for fixed a time. """
        self.message_var.set(message)
        self.after(3000, self.reset_message)

    def reset_message(self) -> None:
        """ Hide message. """
        self.message_var.set("")
