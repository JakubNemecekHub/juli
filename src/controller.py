""" The Controller object for MVC Architecture. """

from src.enums import PlaybackStatus, MixerEnum
from src.model import Model
from src.view import View


class Controller():
    """ Manages Model and View objects. I think its more of a Presenter. """
    def __init__(self, model: Model, view: View):
        self.model: Model = model
        self.view: View = view

    # file handling
    def load_songs(self, path: str) -> None:
        """ Load all songs from given path. """
        loaded: list[str] = self.model.load_songs(path)
        self.view.playlist_frame.populate(loaded)

    # Playback
    def play(self) -> None:
        """ Play song. """
        song, song_id = self.model.get_song() # how to type hint this? (Song | None, int)
        if song:
            self.view.info_frame.set(song)
            self.view.playlist_frame.activate(song_id)
            status: PlaybackStatus = self.model.play(song)
            self.view.status_frame.status(status)

    def pause(self) -> None:
        """ Pause playback. """
        status: PlaybackStatus = self.model.pause()
        if status:
            self.view.status_frame.status(status)

    def stop(self) -> None:
        """ Stop playback. """
        _, song_id = self.model.get_song()
        status: PlaybackStatus = self.model.stop()
        if status:
            self.view.playlist_frame.deselect(song_id)
            self.view.info_frame.reset()
            self.view.status_frame.status(status)

    def previous(self) -> None:
        """ Play previous song if any. """
        song, song_id = self.model.get_previous()
        if song:
            status: PlaybackStatus = self.model.play(song)
            self.view.info_frame.set(song)
            self.view.playlist_frame.activate(song_id)
            self.view.status_frame.status(status)

    def next(self) -> None:
        """ Play next song if any. """
        song, song_id = self.model.get_next()
        if song:
            status: PlaybackStatus = self.model.play(song)
            self.view.info_frame.set(song)
            self.view.playlist_frame.activate(song_id)
            self.view.status_frame.status(status)

    # Volume
    def set_volume(self, volume: float) -> None:
        """ Set volume. """
        self.model.set_volume(volume)

    def mute(self) -> None:
        """ Mute volume. """
        self.model.mute()

    # Play list interface
    def click(self, ignore) -> None:
        """ Handle single click inside playlist. """
        # print("Single click")
        # selection = self.view.get_selection()
        # print(selection)
        # self.model.activate_song(selection)
        # self.play()

    def double_click(self, ignore) -> None:
        """ Handle double click inside playlist. """
        # print("Double click")
        # selection = self.view.get_selection()
        # print(selection)
        # self.model.activate_song(selection)
        # self.play()

    def set_time(self, time: str) -> None:
        """ Set time (in ms) of active. """
        self.model.set_time(int(time))

    def set_mixer(self, mixer: MixerEnum) -> None:
        """ Set Mixer. """
        self.model.set_mixer(mixer)

    ########################################### LOOPS ###########################################
    def loop_runtime(self) -> None:
        """ Update position. """
        state, position = self.model.loop_runtime()
        if state != PlaybackStatus.STOPPED:
            self.view.info_frame.time(position)
        self.view.manager_tab_view.after(100, self.loop_runtime)

    def loop_continue_playback(self) -> None:
        """ Cntinue playing next song from list if any. """
        if self.model.is_playing_and_not_busy():
            if self.model.is_last():
                self.stop()
            else:
                self.next()
        self.view.manager_tab_view.after(100, self.loop_continue_playback)
