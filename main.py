import os
import tkinter as tk
from tkinter.constants import SINGLE, VERTICAL

import pygame


root = tk.Tk()

class MusicPlayer():

    def __init__(self, root):
        self.root = root    # The TkInter window object
        self.root.title("Juli Music Player")
        self.root.geometry("1000x200+100+100") # Height x Width + x + y positions
        pygame.init()
        self.track = tk.StringVar()
        self.status = tk.StringVar()

        # Track Frame for song label and status
        frame_track = tk.LabelFrame(root, text="Song", relief=tk.FLAT)
        frame_track.place(x=0, y=0, width=600, height=100)
        song_track = tk.Label(frame_track, textvariable=self.track, width=20).grid(row=0, column=0, padx=10, pady=5)
        track_status = tk.Label(frame_track, textvariable=self.status, width=20).grid(row=0, column=1, padx=10, pady=5)

        # Button Frame
        frame_button = tk.LabelFrame(self.root, text="Controls", relief=tk.FLAT)
        frame_button.place(x=0, y=100, width=600, height=100)
        btn_play = tk.Button(frame_button, text="Play", command=self.playsong, width=10, height=1).grid(row=0, column=0, padx=10, pady=5)
        btn_pause = tk.Button(frame_button, text="Pause", command=self.pausesong, width=10, height=1).grid(row=0, column=1, padx=10, pady=5)
        # Unpause zatím takto vyřešit nějakým vnitřním stavem a zapracovat do pause tlačítka
        btn_unpause = tk.Button(frame_button, text="UnPause", command=self.unpausesong, width=10, height=1).grid(row=0, column=2, padx=10, pady=5)
        btn_stop = tk.Button(frame_button, text="Stop", command=self.stopsong, width=10, height=1).grid(row=0, column=3, padx=10, pady=5)

        # Playlist Frame
        frame_playlist = tk.LabelFrame(self.root, text="Playlist", relief=tk.FLAT)
        frame_playlist.place(x=600, y=0, width=400, height=200)
        scroll_y_playlist = tk.Scrollbar(frame_playlist, orient=tk.VERTICAL)
        self.playlist = tk.Listbox(frame_playlist, yscrollcommand=scroll_y_playlist.set, selectmode=tk.SINGLE)
        scroll_y_playlist.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_y_playlist.config(command=self.playlist.yview)
        self.playlist.pack(fill=tk.BOTH)

        # Song Directory
        os.chdir("/home/jakub/Music/Blackmores Night/Natures Light (2001)") # User needs to be able to select this folder
        # Fetch Songs
        song_tracks = os.listdir()  # List all types of files
        # Populate Playlist
        for track in song_tracks:
            self.playlist.insert(tk.END, track)

    def playsong(self):
        self.track.set(self.playlist.get(tk.ACTIVE))    # Display selected song
        self.status.set("Playing")                      # Display status
        pygame.mixer.music.load(self.playlist.get(tk.ACTIVE))  # Load selected song
        pygame.mixer.music.play()                              # Play the song

    def pausesong(self):
        self.status.set("Paused")
        pygame.mixer.music.pause()

    def unpausesong(self):
        self.status.set("Playing again")
        pygame.mixer.music.unpause()

    def stopsong(self):
        self.status.set("Stopped")
        pygame.mixer.music.stop()


if __name__ == "__main__":
    player = MusicPlayer(root)
    player.root.mainloop()