import os
import enum
import tkinter as tk
from tkinter import Toplevel, filedialog
from tkinter.constants import SINGLE, VERTICAL

import music_tag

from components.volume import Mixer, FrameVolume
from components.track import FrameTrack

root = tk.Tk()

INITIAL_DIR = r"/home/jakub/Music"
FORMATS = [".mp3", ".vaw", ".ogg"]
TAG_NAMES = ["tracktitle", "artist", "album", "tracknumber"]

class PlaybackStatus(enum.Enum):
    STOPPED = "Stopped"
    PLAYING = "Playing"
    PAUSED = "Paused"


class MusicPlayer():

    def __init__(self, root):
        self.root = root    # The TkInter window object
        self.root.title("Juli Music Player")
        self.root.iconphoto(False, tk.PhotoImage(file = "icon.png"))
        self.root.geometry("1000x300+100+100") # Height x Width + x + y positions
        self.mixer = Mixer()
        # Flags
        self.playback_status = PlaybackStatus.STOPPED
        # Label variables

        # Get default volume
        self.volume = self.mixer.get_volume()

        # Menu
        menu_bar = tk.Menu(root)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Open Folder", command=self.menu_open_folder)
        file_menu.add_command(label="Add Folder", command=self.menu_add_folder)
        file_menu.add_command(label="Add Songs", command=self.menu_add_songs)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.menu_exit)
        menu_bar.add_cascade(label="File", menu=file_menu)
        root.config(menu=menu_bar)

        # Track Frame (for song label and time)
        self.track = FrameTrack(self)

        # Button Frame
        frame_button = tk.LabelFrame(self.root, text="Controls", relief=tk.FLAT)
        frame_button.place(x=0, y=100, width=600, height=100)
        btn_play = tk.Button(frame_button, text="Play", command=self.song_play, width=10, height=1).grid(row=0, column=0, padx=10, pady=5)
        btn_pause = tk.Button(frame_button, text="Pause", command=self.song_pause, width=10, height=1).grid(row=0, column=1, padx=10, pady=5)
        btn_stop = tk.Button(frame_button, text="Stop", command=self.song_stop, width=10, height=1).grid(row=0, column=3, padx=10, pady=5)
        btn_previous = tk.Button(frame_button, text="Previous", command=self.song_previous, width=10, height=1).grid(row=1, column=0, padx=10, pady=5)
        btn_next = tk.Button(frame_button, text="Next", command=self.song_next, width=10, height=1).grid(row=1, column=1, padx=10, pady=5)

        # Volume Frame
        self.frame_volume = FrameVolume(self)

        # Playlist Frame
        frame_playlist = tk.LabelFrame(self.root, text="Playlist", relief=tk.FLAT)
        frame_playlist.place(x=600, y=0, width=400, height=300)
        scroll_y_playlist = tk.Scrollbar(frame_playlist, orient=tk.VERTICAL)
        self.playlistbox = tk.Listbox(frame_playlist, yscrollcommand=scroll_y_playlist.set, selectmode=tk.SINGLE, height=16)
        scroll_y_playlist.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_y_playlist.config(command=self.playlistbox.yview)
        self.playlistbox.pack(fill=tk.BOTH)

        # Status Frame
        self.status_playback = tk.StringVar()
        self.status_files = tk.StringVar()
        frame_status = tk.LabelFrame(self.root, relief=tk.FLAT)
        frame_status.place(x=0, y=275, width=600, height=25)
        tk.Label(frame_status, textvariable=self.status_playback).grid(row=0, column=0, padx=0, pady=0) # track_status
        tk.Label(frame_status, textvariable=self.status_files).grid(row=0, column=1, padx=0, pady=0)    # files_status

        # Song Directory
        # STARTING_DIR = r"Blackmores Night/Natures Light (2001)"
        # STARTING_DIR = r"Violet Sedan Chair"
        STARTING_DIR = r"Mike Oldfield/Light And Shade"
        self.playlist = {}
        self.populate_playlist(os.path.join(INITIAL_DIR, STARTING_DIR))

    def populate_playlist(self, folder: str, append = False):
        # Load files
        loaded_files = {}
        for root_dir, dirs, files in os.walk(folder):
            for file in files:
                # Skip non-supported formats
                if os.path.splitext(file)[1] not in FORMATS:
                    continue
                path = os.path.join(root_dir, file)
                # Load and process tags -> this can be its own function
                tags = music_tag.load_file(path)
                song = {key: tags[key].value for key in TAG_NAMES} # What if song doesn't have tags?
                song_id = f"{song['artist']} - {song['album']} - {song['tracknumber']} - {song['tracktitle']}"
                song["path"] = path
                loaded_files[song_id] = song
        # Check if any songs loaded
        if not loaded_files:
            # No supported songs founds
            self.status_files.set("No files found")
            root.after(3000, lambda : self.status_files.set(""))
            return
        # Delete present songs if not append
        if not append:
            self.playlist.clear()               # playlist
            self.playlistbox.delete(0, tk.END)  # playlistbox
        # Populate playlistbox
        self.playlist = loaded_files.copy()
        for song_id in self.playlist.keys():
            self.playlistbox.insert(tk.END, song_id)

    def menu_exit(self):
        self.root.destroy()

    def menu_open_folder(self):
        dir = filedialog.askdirectory(initialdir=INITIAL_DIR, title="Select a folder")
        if dir:
            # Directory selected
            self.song_stop()    # Stop playing
            self.populate_playlist(dir)

    def menu_add_folder(self):
        dir = filedialog.askdirectory(initialdir=INITIAL_DIR, title="Select a folder")
        if dir:
            # Directory selected
            self.populate_playlist(dir, append=True)

    def menu_add_songs(self):
        FILE_TYPES = [("Music format", ".mp3"), ("Music format", ".vaw"), ("Music format", ".ogg")]
        selection = filedialog.askopenfilenames(initialdir=INITIAL_DIR, title="Select a song", filetypes=FILE_TYPES)
        for song in selection:
            self.playlistbox.insert(tk.END, song)

    def _set_status(self, status: enum.Enum):
        self.status_playback.set(status.value)
        self.playback_status = status

    def song_play(self):
        if not self.playlistbox.curselection():
            # Nothing is selected -> select first song
            self.playlistbox.activate(0)
            self.playlistbox.selection_set(0)
            self.playlistbox.see(0)

        active_song = self.playlistbox.get(tk.ACTIVE)
        self.track.set(active_song)                             # Display selected song
        self._set_status(PlaybackStatus.PLAYING)
        self.mixer.load(self.playlist[active_song]["path"])    # Load selected song
        self.mixer.play()                                      # Play the song

    def song_pause(self):
        if self.playback_status == PlaybackStatus.PLAYING:
            self.mixer.pause()
            self._set_status(PlaybackStatus.PAUSED)
        elif self.playback_status == PlaybackStatus.PAUSED:
            self.mixer.unpause()
            self._set_status(PlaybackStatus.PLAYING)

    def song_stop(self):
        self.mixer.stop()
        self._set_status(PlaybackStatus.STOPPED)
        self.track.clear()                          # Clear song_track label
        self.playlistbox.selection_clear(0, tk.END) # Clear playlist selection
        self.playlistbox.see(0)

    def song_next(self):
        try:
            current_index = self.playlistbox.curselection()[0]
        except IndexError:
            # No Selection -> start from beginning
            current_index = -1

        if current_index < self.playlistbox.size() - 1:
            # Last item not selected
            next_index = current_index + 1
            self.playlistbox.selection_clear(current_index)
            self.playlistbox.activate(next_index)
            self.playlistbox.selection_set(next_index)
            self.playlistbox.see(next_index)

            self.song_play()

    def song_previous(self):
        try:
            current_index = self.playlistbox.curselection()[0]
        except IndexError:
            # No Selection -> do nothing
            return

        if current_index > 0:
            # First item not selected
            next_index = current_index - 1
            self.playlistbox.selection_clear(current_index)
            self.playlistbox.activate(next_index)
            self.playlistbox.selection_set(next_index)
            self.playlistbox.see(next_index)

            self.song_play()

    def loop_runtime(self):
        if self.playback_status == PlaybackStatus.PLAYING:
            self.track.set_run_time(self.mixer.get_pos())
        elif self.playback_status == PlaybackStatus.STOPPED:
            self.track.clear_run_time()

        root.after(100, self.loop_runtime)

    def loop_continuity(self):
        if self.playback_status == PlaybackStatus.PLAYING and not self.mixer.get_busy():
            # If at the last song of the playlist -> STOPPED
            current_index = self.playlistbox.curselection()[0]
            if current_index == self.playlistbox.size() - 1:
                self.playback_status = PlaybackStatus.STOPPED
            else:
                # Player is playing but the mixer is not busy
                # Not at the last song in playlist
                # -> play next song
                self.song_next()

        root.after(100, self.loop_continuity)

if __name__ == "__main__":
    player = MusicPlayer(root)
    player.loop_runtime()
    player.loop_continuity()
    player.root.mainloop()
