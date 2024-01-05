""" Status Bar """

import customtkinter as ctk


class StatusBar():

    def __init__(self, root: ctk.CTk):

        self._status = ctk.StringVar()
        self._message = ctk.StringVar()

        self.frame = ctk.CTkFrame(root) 
        # Status label
        l_status = ctk.CTkLabel(self.frame, textvariable=self._status)
        l_status.grid(row=0, column=0, padx=5, pady=0)
        # Message label
        l_message = ctk.CTkLabel(self.frame, textvariable=self._message)
        l_message.grid(row=0, column=1, padx=5, pady=0) 

    def set_status(self, status: str) -> None:
        self._status.set(status)

    def set_message(self, status: str) -> None:
        self._message.set(status)
        # Hide message after 3s
        self.frame.after(3000, self.reset_message)

    def reset_status(self) -> None:
        self._status.set("")

    def reset_message(self) -> None:
        self._message.set("")
