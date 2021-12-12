""" Status Bar """

import tkinter as tk


class StatusBar():

    def __init__(self, master):

        self.master = master

        self.status_playback = tk.StringVar()
        self.status_files = tk.StringVar()
        frame_status = tk.LabelFrame(self.master.root, relief=tk.FLAT)
        frame_status.place(x=0, y=275, width=600, height=25)
        tk.Label(frame_status, textvariable=self.status_playback).grid(row=0, column=0, padx=5, pady=0) # track_status
        tk.Label(frame_status, textvariable=self.status_files).grid(row=0, column=1, padx=5, pady=0)    # files_status

    def set_playback_status(self, status: str):
        self.status_playback.set(status)

    def set_files_status(self, status: str):
        self.status_files.set(status)