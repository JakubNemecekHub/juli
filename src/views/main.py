import customtkinter as ctk

from ..enums import PlaybackStatus

class StatusFrame(ctk.CTkFrame):

    def __init__(self, root):
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
        self.status_var.set(status.value)

    def message(self, message: str) -> None:
        self.message_var.set(message)
        self.after(3000, self.reset_message)

    def reset_message(self) -> None:
        self.message_var.set("")
