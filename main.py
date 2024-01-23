import os

import customtkinter as ctk
from PIL import ImageTk

from src.view import View
from src.model import Model
from src.controller import Controller


class MusicPlayer():

    def __init__(self):
        ctk.set_appearance_mode("dark")     # May change to "system" in the future
        self.root = ctk.CTk()               # The Custom TkInter window object
        self.root.title("Juli Music Player")
        icon = ImageTk.PhotoImage(file=os.path.join("icons", "icon.png"))
        self.root.wm_iconbitmap()
        self.root.iconphoto(False, icon)
        self.root.geometry("400x550+100+100") # Width x Height + x + y positions

        self.model = Model()
        self.view = View(self.root)
        self.controller = Controller(self.model, self.view)
        self.view.init(self.controller)

        self.controller.load_songs(self.model.STARTING_DIR)

if __name__ == "__main__":
    player = MusicPlayer()
    player.controller.loop_runtime()
    player.controller.loop_continue_playback()
    player.root.mainloop()
