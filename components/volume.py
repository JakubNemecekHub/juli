""" Volume Frame """

import tkinter as tk


class VolumeControls():

    def __init__(self, master):

        self.master = master

        # Flags
        self.mute = tk.BooleanVar()

        # Get default volume
        self.volume = self.master.mixer.get_volume()

        frame_volume = tk.LabelFrame(self.master.root, text="Volume Controls", relief=tk.FLAT)
        frame_volume.place(x=0, y=200, width=600, height=75)
        scl_volume = tk.Scale(frame_volume, showvalue=0, command=self.set_volume, orient=tk.HORIZONTAL, width=10)
        scl_volume.grid(row=0, column=0, columnspan=2, padx=10, pady=5)
        scl_volume.set(self.volume * 100)
        # Mute checkbox
        tk.Checkbutton(frame_volume, text="Mute", variable=self.mute, command=self.song_mute).grid(row=0, column=3, padx=10, pady=5)

    def set_volume(self, volume):
        self.master.mixer.set_volume(int(volume) / 100)
        if self.mute.get():
            self.mute.set(False)

    def song_mute(self):
        if self.mute.get():                             # Activate mute
            self.volume = self.master.mixer.get_volume()
            self.master.mixer.set_volume(0.0)
        else:                                           # Deactivate mute
            self.master.mixer.set_volume(self.volume)
