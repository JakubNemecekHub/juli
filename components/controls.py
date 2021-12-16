""" Control Buttons Frame """

import tkinter as tk


class Controls():

    def __init__(self, master):

        self.master = master

        frame_button = tk.LabelFrame(master.root, text="Controls", relief=tk.FLAT)
        frame_button.place(x=0, y=100, width=600, height=100)
        btn_play = tk.Button(frame_button, text="Play", command=self.song_play).grid(row=0, column=0, padx=10, pady=2.5)
        btn_pause = tk.Button(frame_button, text="Pause", command=self.song_pause).grid(row=0, column=1, padx=10, pady=2.5)
        btn_stop = tk.Button(frame_button, text="Stop", command=self.song_stop).grid(row=0, column=3, padx=10, pady=2.5)
        btn_previous = tk.Button(frame_button, text="Previous", command=self.song_previous).grid(row=1, column=0, padx=10, pady=2.5)
        btn_next = tk.Button(frame_button, text="Next", command=self.song_next).grid(row=1, column=1, padx=10, pady=2.5)
        self.scl_time = tk.Scale(frame_button, showvalue=0, command=self.song_set_position, orient=tk.HORIZONTAL)
        self.scl_time.grid(row=1, column=2, columnspan=3)
        self.scl_time.set(0)

    def _set_status(self, status):
        self.master.status_bar.set_playback_status(status.value)
        self.master.playback_status = status
    
    def song_play(self):
        # Nothing is selected -> select first song
        if not self.master.playlist.is_selected():
            self.master.playlist.select(0)

        active_song = self.master.playlist.get_active()
        self.master.mixer.load(self.master.playlist.list[active_song]["path"])  # Load selected song
        self.master.track.set(active_song)                                      # Display selected song
        self._set_status(self.master.status_enum.PLAYING)                       # Update Status bar
        self.master.mixer.play()                                                # Play the song

    def song_pause(self):
        if self.master.playback_status == self.master.status_enum.PLAYING:
            self.master.mixer.pause()
            self._set_status(self.master.status_enum.PAUSED)
        elif self.master.playback_status == self.master.status_enum.PAUSED:
            self.master.mixer.unpause()
            self._set_status(self.master.status_enum.PLAYING)

    def song_stop(self):
        self.master.mixer.stop()
        self._set_status(self.master.status_enum.STOPPED)
        self.master.track.clear()              # Clear song_track label
        self.master.playlist.clear_selection() # Clear playlist selection

    def song_next(self):
        try:
            current_index = self.master.playlist.get_index()
        except IndexError:
            # No Selection -> start from beginning
            current_index = -1

        if current_index < self.master.playlist.size() - 1:
            # Last item not selected
            next_index = current_index + 1
            self.master.playlist.select(next_index)

            self.song_play()

    def song_previous(self):
        try:
            current_index = self.master.playlist.get_index()
        except IndexError:
            # No Selection -> do nothing
            return

        if current_index > 0:
            # First item not selected
            next_index = current_index - 1
            self.master.playlist.select(next_index)

            self.song_play()

    def song_set_position(self, position: int):
        duration = self.master.mixer.get_duration()
        value = duration * (int(position) / 100)
