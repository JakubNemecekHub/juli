from enum import Enum

# Enums to separate module?
class PlaybackStatus(Enum):
    STOPPED = "Stopped"
    PLAYING = "Playing"
    PAUSED = "Paused"

# Do I really need this?
class VolumeState(Enum):
    UNMUTE = "Unmute"
    MUTE = "Mute"
