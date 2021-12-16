""" Tack Frame """

import time
import tkinter as tk


class TrackFrame():

    def __init__(self, master):

        self.master = master

        # Label variables
        self.track = tk.StringVar()
        self.run_time = tk.StringVar()
        self.duration = tk.StringVar()
        self._duration = 0

        frame_track = tk.LabelFrame(self.master.root, text="Song", relief=tk.FLAT)
        frame_track.place(x=0, y=0, width=600, height=100)
        song_track = tk.Label(frame_track, textvariable=self.track).grid(row=0, column=0, padx=10, pady=5)
        track_time = tk.Label(frame_track, textvariable=self.run_time, width=20).grid(row=1, column=0, padx=10, pady=5)
        track_duration = tk.Label(frame_track, textvariable=self.duration, width=20).grid(row=1, column=1, padx=10, pady=5)

    def set(self, label: str):
        # Set track label
        _label = self.master.playlist.list[label]["tracktitle"]
        self.track.set(_label)
        # Set track duration
        self._duration = self.master.playlist.list[label]["duration"]
        if self._duration:
            self.duration.set(self.run_time_str(self._duration))

    def clear(self):
        self.track.set("")      # Clear track label
        self.duration.set("")   # Clear track duration

    def run_time_str(self, ms: int) -> str:
        """ Converts input milliseconds into formated time string """

        # Show hours only when necessary
        _format = "%M:%S"
        if ms >= 3600000:
            _format = "%H:%M:%S"

        return time.strftime(_format, time.gmtime(ms // 1000))     

    def loop_runtime(self):
        if self.master.playback_status == self.master.status_enum.PLAYING:
            # duration = int(self.duration.get())
            position = self.master.mixer.get_pos()
            self.run_time.set(self.run_time_str(position))                        # Show time
            print(position / self._duration * 100)
            self.master.controls.scl_time.set(position / self._duration * 100)    # Update time scale
        elif self.master.playback_status == self.master.status_enum.STOPPED:
            self.run_time.set("")
            self.master.controls.scl_time.set(0)

        self.master.root.after(100, self.loop_runtime)
