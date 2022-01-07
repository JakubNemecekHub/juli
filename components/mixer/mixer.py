""" Abstract class for Mixer """

from abc import ABC, abstractmethod


class Mixer(ABC):

    @abstractmethod
    def load(self, file: str):
        pass

    @abstractmethod
    def play(self):
        pass

    @abstractmethod
    def pause(self):
        pass

    @abstractmethod
    def unpause(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    def get_duration(self) -> int:
        """ Return song duration in milliseconds. """
        return None

    @abstractmethod
    def get_position(self) -> int:
        """ Returns position in milliseconds. """
        pass

    def set_position(self, position: int):
        """ Takes in milliseconds. """
        pass

    @abstractmethod
    def get_busy(self) -> bool:
        pass

    @abstractmethod
    def get_volume(self) -> float:
        pass

    @abstractmethod
    def set_volume(self, volume: float):
        pass

    @abstractmethod
    def supported_formats(self) -> list[str]:
        pass

    @abstractmethod
    def file_types(self) -> list[str]:
        pass
