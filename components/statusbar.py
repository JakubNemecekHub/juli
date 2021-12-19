""" Status Bar """

import tkinter as tk


class StatusBar():

    def __init__(self):

        self._status = tk.StringVar()
        self._message = tk.StringVar()

        self.frame = tk.LabelFrame(relief=tk.FLAT) 
        # Status label
        l_status = tk.Label(self.frame, textvariable=self._status)
        l_status.grid(row=0, column=0, padx=5, pady=0)
        # Message label
        l_message = tk.Label(self.frame, textvariable=self._message)
        l_message.grid(row=0, column=1, padx=5, pady=0) 

    def set_status(self, status: str) -> None:
        self._status.set(status)

    def set_message(self, status: str) -> None:
        self._message.set(status)

    def reset_status(self) -> None:
        self._status.set("")

    def reset_message(self) -> None:
        self._message.set("")
