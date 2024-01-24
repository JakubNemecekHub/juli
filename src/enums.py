"""Various Enumes use throughout the code."""

from enum import Enum

class PlaybackStatus(Enum):
    """State of the Mixer."""
    STOPPED = "Stopped"
    PLAYING = "Playing"
    PAUSED = "Paused"

# Do I really need this?
class VolumeState(Enum):
    """State of volume."""
    UNMUTE = "Unmute"
    MUTE = "Mute"

class MixerEnum(Enum):
    """Aviable Mixers."""
    PYGAME = 1
    JUST_PLAYBACK = 2
