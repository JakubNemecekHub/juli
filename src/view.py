import customtkinter as ctk

from .views.main import StatusFrame
from .views.player import ControlFrame, VolumeFrame, InfoFrame, PlayListFrame
from .views.library import FolderFrame, MixerFrame

class View():

    def __init__(self, root):
        self.root = root
        self.controller = None

    def init(self, controller) -> None:
        self.controller = controller
        # Create tabs for music player and library management 
        self.manager_tab_view = ctk.CTkTabview(self.root)
        self.tab_player = self.manager_tab_view.add("Player")
        self.tab_library = self.manager_tab_view.add("Library")
        self.manager_tab_view.set("Player")
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=50)
        self.manager_tab_view.grid(row=0, column=0, sticky="nsew")

        self.status_frame = StatusFrame(self.root)
        self.status_frame.grid(row=1, column=0, sticky="ew")
        self.root.grid_rowconfigure(1, weight=1)

        # Player tab
        self.tab_player.grid_columnconfigure(0, weight=1)
        self.tab_player.grid_rowconfigure((0, 1, 2), weight=1)
        self.tab_player.grid_rowconfigure(3, weight=100)  # Playlist
        self.control_frame = ControlFrame(self.tab_player, self.controller)
        self.control_frame.grid(row=0, column=0, sticky="ew")
        self.volume_frame = VolumeFrame(self.tab_player, self.controller)
        self.volume_frame.grid(row=1, column=0, sticky="ew")
        self.info_frame = InfoFrame(self.tab_player, self.controller)
        self.info_frame.grid(row=2, column=0, sticky="ew")
        self.playlist_frame = PlayListFrame(self.tab_player, self.controller)
        self.playlist_frame.grid(row=3, column=0, sticky="nsew")

        # Library tab
        self.tab_library.grid_columnconfigure(0, weight=1)
        self.tab_library.grid_rowconfigure((0, 1), weight=1)
        self.tab_library.grid_rowconfigure(2, weight=10)
        self.folder_frame = FolderFrame(self.tab_library, self.controller)
        self.folder_frame.grid(row=0, column=0, sticky="ew")
        self.mixer_frame = MixerFrame(self.tab_library, self.controller)
        self.mixer_frame.grid(row=1, column=0, sticky="ew")

  