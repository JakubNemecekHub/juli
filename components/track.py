""" Tack Frame """

import tkinter as tk


class FrameTrack():

    def __init__(self, master):

        self.master = master

        # Label variables
        self.track = tk.StringVar()
        self.run_time = tk.StringVar()

        frame_track = tk.LabelFrame(master.root, text="Song", relief=tk.FLAT)
        frame_track.place(x=0, y=0, width=600, height=100)
        song_track = tk.Label(frame_track, textvariable=self.track).grid(row=0, column=0, padx=10, pady=5)
        track_time = tk.Label(frame_track, textvariable=self.run_time, width=20).grid(row=1, column=0, padx=10, pady=5)

    def set(self, label: str):
        self.track.set(label)

    def clear(self):
        self.track.set("")

    def run_time_str(self, ms: int) -> str:
        """ Converts input milliseconds into formated time string """
        
        hours = ms // 3600000
        ms_after_hours = ms % 3600000
        minutes = ms_after_hours // 60000
        ms_after_minutes = ms_after_hours % 60000
        seconds = ms_after_minutes // 1000
        # ms_left = ms_after_minutes % 1000

        time_str = ""
        if hours != 0:
            time_str += f"{hours:02d}:"

        time_str += f"{minutes:02d}:{seconds:02d}"
        
        return time_str

    def set_run_time(self, time: float):
        self.run_time.set(self.run_time_str(time))

    def clear_run_time(self):
        self.run_time.set("")