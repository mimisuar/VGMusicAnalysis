# this is a magic class that represents the game dictionary. :)
from typing import Dict, List, Optional, Generator, Union
from music21 import stream
import vgmusic

def _is_subset(list1: List, list2: List) -> bool:
    """
    Returns True when list1 is a subset of list2
    """
    for element in list1:
        if element not in list2:
            return False
    return True

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

    def load_dict(self, game_dict: Dict):
        self.genres: List[str] = game_dict.get("genres")
        self.themes: List[str] = game_dict.get("themes")
        self.console: str = game_dict.get("console")
        #self.loadable: Dict[str, bool] =  game_dict.get("loadable")
        self.songs: List[str] = []
        for song_title in game_dict["songs"]:
            if game_dict["songs"][song_title]["loadable"]:
                self.songs.append(song_title)
        self.year: int = game_dict.get("year")
        self.id: int = game_dict.get("id")

    def fetch(self, song_title: str) -> Optional[stream.Stream]:
        #if song_title in self.loadable and not self.loadable[song_title]:
        #    raise SkippedSongException("{0}/{1} marked unloadable. Skipping.".format(self.name, song_title))

        try:
            return vgmusic.fetch(self.name, song_title)
        except:
            raise FailedFetchException("{0}/{1} failed to load".format(self.name, song_title))
    
    def fetch_all_songs(self) -> Generator[stream.Stream, None, None]:
        for song_title in self.songs:
            if self.is_remix(song_title):
                continue
            try:
                yield self.fetch(song_title)
            except Exception as e:
                print(e)
    
    def has_genres(self, genres: Union[str, List[str]]) -> bool:
        if isinstance(genres, str):
            return genres in self.genres
        elif isinstance(genres, list):
            for genre in genres:
                if _is_subset(genres, self.genres):
                    return False
            return True
        return False

    def has_themes(self, themes: Union[str, List[str]]) -> bool:
        if isinstance(themes, str):
            return themes in self.themes
        elif isinstance(themes, list):
            for genre in themes:
                if _is_subset(themes, self.themes):
                    return False
            return True
        return False

    def is_remix(self, song_title: str) -> bool:
        return "remix" in song_title.lower() or "xg" in song_title.lower()
