""" Implementation of Mixer using pygame.mixer """

from pygame import mixer

from .mixer import Mixer


class PygameMixer(Mixer):

    def __init__(self):
        print("Pygame")
        mixer.init()

    def load(self, file: str):
        mixer.music.load(file)

    def play(self):
        mixer.music.play()

    def pause(self):
        mixer.music.pause()

    def unpause(self):
        mixer.music.unpause()

    def stop(self):
        mixer.music.stop()

    def get_pos(self) -> int:
        return mixer.music.get_pos() # returns milliseconds

    def get_busy(self) -> bool:
        return mixer.music.get_busy()

    def get_volume(self) -> float:
        return mixer.music.get_volume()

    def set_volume(self, volume: float):
        mixer.music.set_volume(volume)
