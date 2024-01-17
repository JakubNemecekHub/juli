import os

import customtkinter as ctk
from PIL import ImageTk

from components.view import View
from components.model import Model
from components.controller import Controller


class MusicPlayer():

    def __init__(self):
        ctk.set_appearance_mode("dark")     # May change to "system" in the future
        self.root = ctk.CTk()               # The Custom TkInter window object
        self.root.title("Juli Music Player")
        icon = ImageTk.PhotoImage(file=os.path.join("icons", "icon.png"))
        self.root.wm_iconbitmap()
        self.root.iconphoto(False, icon)
        self.root.geometry("600x550+100+100") # Width x Height + x + y positions

        self.model = Model()
        self.view = View(self.root)
        self.controller = Controller(self.model, self.view)

        # Bind Controller methods to View
        self.view.bind_commands(self.controller.play, self.controller.pause, self.controller.stop, self.controller.previous, self.controller.next)
        self.view.bind_load(self.controller.load_songs)
        self.view.bind_playlist(self.controller.click, self.controller.double_click)
        self.view.bind_volume(self.controller.set_volume)
        self.view.bind_mute(self.controller.mute)
        self.view.bind_time(self.controller.set_time)

        self.view.bind_mixer_selection(self.controller.set_mixer, self.model.mixer_var)
        self.controller.load_songs(self.model.STARTING_DIR)


if __name__ == "__main__":
    player = MusicPlayer()
    player.controller.loop_runtime()
    player.controller.loop_continue_playback()
    player.root.mainloop()
