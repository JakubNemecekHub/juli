import time
import customtkinter as ctk

# Define Protocol for Song?


class PlayBar():

    def __init__(self, root: ctk.CTk):

        # Label variables
        self.track = ctk.StringVar()
        self.time = ctk.StringVar()
        self.duration = ctk.StringVar()

        self.frame = ctk.CTkFrame(root)
        l_track = ctk.CTkLabel(self.frame, textvariable=self.track)
        l_track.grid(row=0, column=0, padx=10, pady=5)
        l_time = ctk.CTkLabel(self.frame, textvariable=self.time, width=20)
        l_time.grid(row=1, column=0, padx=10, pady=5)
        l_duration = ctk.CTkLabel(self.frame, textvariable=self.duration, width=20)
        l_duration.grid(row=1, column=1, padx=10, pady=5)

    def set(self, song) -> None:
        self.track.set(song.tracktitle) # Set track label
        # Set track duration
        if song.duration:
            self.duration.set(self.time_str(song.duration))

    def reset_song(self) -> None:
        self.track.set("")      # Clear track label
        self.duration.set("")   # Clear track duration

    def set_time(self, time: int) -> None:
        self.time.set(self.time_str(time))

    def reset_time(self) -> None:
        self.time.set("")

    def time_str(self, ms: int) -> str:
        """ Converts input milliseconds into formated time string """

        # Show hours only when necessary
        _format = "%M:%S"
        if ms >= 3600000:
            _format = "%H:%M:%S"

        return time.strftime(_format, time.gmtime(ms // 1000))     
