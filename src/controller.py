from .enums import *
from .model import Model, Song
from .view import View


class Controller():

    def __init__(self, model: Model, view: View):
        self.model: Model = model
        self.view: View = view

    # file handling
    def load_songs(self, path: str) -> None:
        loaded: list[str] = self.model.load_songs(path)
        self.view.playlist_frame.populate(loaded)

    # Playback
    def play(self) -> None:
        song, id = self.model.get_song() # how to type hint this? (Song | None, int)
        if song:                             
            self.view.info_frame.update(song)
            self.view.playlist_frame.update(id)
            status: PlaybackStatus = self.model.play(song)
            self.view.status_frame.status(status)

    def pause(self) -> None:
        status: PlaybackStatus = self.model.pause()
        if status:
            self.view.status_frame.status(status)

    def stop(self) -> None:
        song, id = self.model.get_song()
        status: PlaybackStatus = self.model.stop()
        if status:
            self.view.playlist_frame.deselect(id)
            self.view.info_frame.reset()
            self.view.status_frame.status(status)

    def previous(self) -> None:
        song, id = self.model.get_previous()
        if song:
            status: PlaybackStatus = self.model.play(song)
            self.view.info_frame.update(song)
            self.view.playlist_frame.update(id)
            self.view.status_frame.status(status)

    def next(self) -> None:
        song, id = self.model.get_next()
        if song:
            status: PlaybackStatus = self.model.play(song)
            self.view.info_frame.update(song)
            self.view.playlist_frame.update(id)
            self.view.status_frame.status(status)

    # Volume
    def set_volume(self, volume: float) -> None:
        self.model.set_volume(volume)
    
    def mute(self) -> None:
        self.model.mute()

    # Play list interface
    def click(self, ignore) -> None:
        # print("Single click")
        # selection = self.view.get_selection()
        # print(selection)
        # self.model.activate_song(selection)
        # self.play()
        pass

    def double_click(self, ignore) -> None:
        # print("Double click")
        # selection = self.view.get_selection()
        # print(selection)
        # self.model.activate_song(selection)
        # self.play()
        pass

    def set_time(self, time: str) -> None:
        self.model.set_time(int(time))

    def set_mixer(self, mixer: MixerEnum) -> None:
        self.model.set_mixer(mixer)

    ########################################### LOOPS ###########################################
    def loop_runtime(self) -> None:
        state, position = self.model.loop_runtime()
        if state != PlaybackStatus.STOPPED:
            self.view.info_frame.time(position)
        self.view.manager_tab_view.after(100, self.loop_runtime)

    def loop_continue_playback(self) -> None:
        if self.model.is_playing_and_not_busy():
            if self.model._is_last():
                self.stop()
            else:
                self.next()
        self.view.manager_tab_view.after(100, self.loop_continue_playback)
