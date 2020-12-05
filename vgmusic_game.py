# this is a magic class that represents the game dictionary. :)
from typing import Dict, Optional, Generator
from music21 import stream
import vgmusic

class SkippedSongException(Exception):
    def __repr__(self):
        return "SkippedSongException: " + Exception.__str__(self)

class FailedFetchException(Exception):
    def __repr__(self):
        return "FailedFetchException: " + Exception.__str__(self)

class Game:
    def __init__(self, game_name: str, game_dict: Dict):
        self.name = game_name
        self.load_dict(game_dict)

    def load_dict(self, game_dict):
        self.genres = game_dict["genres"]
        self.themes = game_dict["themes"]
        self.console = game_dict["console"]
        self.loadable =  game_dict["loadable"]
        self.songs = [song_title for song_title in game_dict["songs"]]
        self.year = game_dict["year"]
        self.id = game_dict["id"]

    def fetch(self, song_title: str) -> Optional[stream.Stream]:
        if song_title in self.loadable and not self.loadable[song_title]:
            raise SkippedSongException("{0}/{1} marked unloadable. Skipping.".format(self.name, song_title))

        try:
            return vgmusic.fetch(self.name, song_title)
        except:
            raise FailedFetchException("{0}/{1} failed to load".format(self.name, song_title))
    
    def fetch_all_songs(self) -> Generator[stream.Stream, None, None]:
        for song_title in self.songs:
            try:
                yield self.fetch(song_title)
            except Exception as e:
                print(e)
    
