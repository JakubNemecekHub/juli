import tkinter as tk

from components.manager import Manager


class MusicPlayer():

    def __init__(self):
        self.root = tk.Tk()    # The TkInter window object
        self.root.title("Juli Music Player")
        self.root.iconphoto(False, tk.PhotoImage(file="icon.png"))
        self.root.geometry("400x550+100+100") # Width x Height + x + y positions

        self.manager = Manager(self.root)


if __name__ == "__main__":
    player = MusicPlayer()
    player.manager.loop_runtime()
    player.manager.continue_playback()
    player.root.mainloop()
