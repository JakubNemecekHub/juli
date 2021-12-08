import os
import enum
import tkinter as tk
from tkinter.constants import SINGLE, VERTICAL

import pygame


root = tk.Tk()


class PlaybackStatus(enum.Enum):
    STOPPED = "Stopped"
    PLAYING = "Playing"
    PAUSED = "Paused"


class VolumeStatus(enum.Enum):
    MUTE = 0
    UNMUTE = 1


class MusicPlayer():

    def __init__(self, root):
        self.root = root    # The TkInter window object
        self.root.title("Juli Music Player")
        self.root.iconphoto(False, tk.PhotoImage(file = "icon.png"))
        self.root.geometry("1000x275+100+100") # Height x Width + x + y positions
        pygame.init()
        self.track = tk.StringVar()
        self.playback_status = PlaybackStatus.STOPPED
        self.status = tk.StringVar()
        self.volume = pygame.mixer.music.get_volume()
        self.mute = VolumeStatus.UNMUTE

        # Track Frame for song label and status
        frame_track = tk.LabelFrame(root, text="Song", relief=tk.FLAT)
        frame_track.place(x=0, y=0, width=600, height=100)
        song_track = tk.Label(frame_track, textvariable=self.track, width=20).grid(row=0, column=0, padx=10, pady=5)
        track_status = tk.Label(frame_track, textvariable=self.status, width=20).grid(row=0, column=1, padx=10, pady=5)

        # Button Frame
        frame_button = tk.LabelFrame(self.root, text="Controls", relief=tk.FLAT)
        frame_button.place(x=0, y=100, width=600, height=100)
        btn_play = tk.Button(frame_button, text="Play", command=self.song_play, width=10, height=1).grid(row=0, column=0, padx=10, pady=5)
        btn_pause = tk.Button(frame_button, text="Pause", command=self.song_pause, width=10, height=1).grid(row=0, column=1, padx=10, pady=5)
        btn_stop = tk.Button(frame_button, text="Stop", command=self.song_stop, width=10, height=1).grid(row=0, column=3, padx=10, pady=5)
        btn_next = tk.Button(frame_button, text="Next", command=self.song_next, width=10, height=1).grid(row=1, column=0, padx=10, pady=5)
        btn_previous = tk.Button(frame_button, text="Previous", command=self.song_previous, width=10, height=1).grid(row=1, column=1, padx=10, pady=5)
        
        # Volume Frame
        frame_volume = tk.LabelFrame(self.root, text="Volume Controls", relief=tk.FLAT)
        frame_volume.place(x=0, y=200, width=600, height=75)
        scl_volume = tk.Scale(frame_volume, showvalue=0, command=self.set_volume, orient=tk.HORIZONTAL, width=10)
        scl_volume.grid(row=0, column=0, columnspan=2, padx=10, pady=5)
        scl_volume.set(self.volume * 100)
        btn_mute = tk.Button(frame_volume, text="Mute", command=self.song_mute, width=10, height=1).grid(row=0, column=2, padx=10, pady=5)
        
        # Playlist Frame
        frame_playlist = tk.LabelFrame(self.root, text="Playlist", relief=tk.FLAT)
        frame_playlist.place(x=600, y=0, width=400, height=275)
        scroll_y_playlist = tk.Scrollbar(frame_playlist, orient=tk.VERTICAL)
        self.playlist = tk.Listbox(frame_playlist, yscrollcommand=scroll_y_playlist.set, selectmode=tk.SINGLE, height=14)
        scroll_y_playlist.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_y_playlist.config(command=self.playlist.yview)
        self.playlist.pack(fill=tk.BOTH)

        # Song Directory
        os.chdir("/home/jakub/Music/Blackmores Night/Natures Light (2001)")
        # Fetch Songs
        song_tracks = os.listdir()
        # Populate Playlist
        for track in song_tracks:
            self.playlist.insert(tk.END, track)

    def _set_status(self, status: enum.Enum):
        self.status.set(status.value)
        self.playback_status = status

    def song_play(self):
        if not self.playlist.curselection():
            # Nothing is selected -> select first song
            self.playlist.activate(0)
            self.playlist.selection_set(0)
            self.playlist.see(0)

        self.track.set(self.playlist.get(tk.ACTIVE))            # Display selected song
        self._set_status(PlaybackStatus.PLAYING)
        pygame.mixer.music.load(self.playlist.get(tk.ACTIVE))   # Load selected song
        pygame.mixer.music.play()                               # Play the song

    def song_pause(self):
        if self.playback_status == PlaybackStatus.PLAYING:
            pygame.mixer.music.pause()
            self._set_status(PlaybackStatus.PAUSED)
        elif self.playback_status == PlaybackStatus.PAUSED:
            pygame.mixer.music.unpause()
            self._set_status(PlaybackStatus.PLAYING)

    def song_stop(self):
        pygame.mixer.music.stop()
        self._set_status(PlaybackStatus.STOPPED)
        self.track.set("")                          # Clear song_track label
        self.playlist.selection_clear(0, tk.END)    # Clear playlist selection
        self.playlist.see(0)

    def song_next(self):
        try:
            current_index = self.playlist.curselection()[0]
        except IndexError:
            # No Selection -> start from beginning
            current_index = -1

        if current_index < self.playlist.size() - 1:
            # Last item not selected
            next_index = current_index + 1
            self.playlist.selection_clear(current_index)
            self.playlist.activate(next_index)
            self.playlist.selection_set(next_index)
            self.playlist.see(next_index)

            self.song_play()

    def song_previous(self):
        try:
            current_index = self.playlist.curselection()[0]
        except IndexError:
            # No Selection -> do nothing
            return

        if current_index > 0:
            # First item not selected
            next_index = current_index - 1
            self.playlist.selection_clear(current_index)
            self.playlist.activate(next_index)
            self.playlist.selection_set(next_index)
            self.playlist.see(next_index)

            self.song_play()

    def set_volume(self, volume):
        pygame.mixer.music.set_volume(int(volume) / 100)

    def song_mute(self):
        if self.mute == VolumeStatus.UNMUTE:
            self.mute = VolumeStatus.MUTE
            self.volume = pygame.mixer.music.get_volume()
            pygame.mixer.music.set_volume(0.0)
        elif self.mute == VolumeStatus.MUTE:
            self.mute = VolumeStatus.UNMUTE
            pygame.mixer.music.set_volume(self.volume)


if __name__ == "__main__":
    player = MusicPlayer(root)
    player.root.mainloop()