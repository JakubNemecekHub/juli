""" Implementation of Mixer using just_playback """

from just_playback import Playback

from .mixer import Mixer


class JustMixer(Mixer):
    
    def __init__(self):
        print("JustPlayback")
        self.mixer = Playback()
        self.FORMATS = [".mp3", ".vaw", ".ogg", ".flac"]

    def load(self, file: str):
        # Check formats?
        self.mixer.load_file(file)

    def play(self):
        self.mixer.play()

    def pause(self):
        self.mixer.pause()

    def unpause(self):
        self.mixer.resume()

    def stop(self):
        self.mixer.stop()

    def get_duration(self) -> int:
        return int(self.mixer.duration * 1000)

    def get_position(self) -> int:
        # normally returns seconds as float
        return int(self.mixer.curr_pos * 1000)

    def set_position(self, position: int):
        position_s = position // 1000
        self.mixer.seek(position_s)

    def get_busy(self) -> bool:
        return self.mixer.active

    def get_volume(self) -> float:
        return self.mixer.volume

    def set_volume(self, volume: float):
        self.mixer.set_volume(volume)

    def supported_formats(self) -> list[str]:
        return self.FORMATS

    def file_types(self) -> list[str]:
        return [("Music format", format) for format in self.FORMATS]
