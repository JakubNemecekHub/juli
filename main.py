import os

import customtkinter as ctk
from PIL import ImageTk

from components.manager import Manager


class MusicPlayer():

    def __init__(self):
        ctk.set_appearance_mode("dark")     # May change to "system" in the future
        self.root = ctk.CTk()               # The Custom TkInter window object
        self.root.title("Juli Music Player")
        icon = ImageTk.PhotoImage(file=os.path.join("icons", "icon.png"))
        self.root.wm_iconbitmap()
        self.root.iconphoto(False, icon)
        self.root.geometry("600x550+100+100") # Width x Height + x + y positions

        self.manager = Manager(self.root)


if __name__ == "__main__":
    player = MusicPlayer()
    player.manager.loop_runtime()
    player.manager.continue_playback()
    player.root.mainloop()
