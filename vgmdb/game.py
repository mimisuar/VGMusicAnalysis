from __future__ import annotations
import vgmdb.genre, vgmdb.theme, vgmdb.platform

class Game:
    def __init__(self) -> None:
        self._id = 0
        self._genres = []
        self._themes = []
        self._year = 0
        self._platforms = []
        self._name = ""
        self._songs = {}

    def __eq__(self, other) -> bool:
        return self.id == other.id and self.id > 0

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, value: int) -> None:
        assert isinstance(value, int), "Invalid ID type."
        self._id = value

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        assert isinstance(value, str), "Invalid name type."
        self._name = value

    @property
    def year(self) -> int:
        return self._year

    @year.setter
    def year(self, value: int):
        assert isinstance(value, int), "Invalid year type."
        self._year = value


    def add_song(self, song_name: str, song_url: str) -> None:
        self._songs[song_name] = song_url

    def add_genre(self, genre: vgmdb.genre.Genre) -> None:
        self._genres.append(genre)

    def add_theme(self, theme: vgmdb.theme.Theme) -> None:
        self._themes.append(theme)

    def add_platform(self, platform: vgmdb.platform.Platform) -> None:
        self._platforms.append(platform)

    def encode(self) -> dict:
        return {
            "id": self._id,
            "name": self._name,
            "songs": self._songs,
            "genres": [genre.encode() for genre in self._genres],
            "themes": [theme.encode() for theme in self._themes],
            "platforms": [pform.encode() for pform in self._platforms],
        }

    @classmethod
    def decode(cls, dict_inst: dict) -> Game:
        assert isinstance(dict_inst, dict), "Game decode only works on dictionarys."
        game_inst = cls()
        game_inst._id = dict_inst.get("id", 0)
        game_inst._name = dict_inst.get("name", "")
        game_inst._consoles = dict_inst.get("consoles", [])
        game_inst._genres = [vgmdb.genre.Genre.decode(id) for id in dict_inst.get("genres", [])]
        game_inst._themes = [vgmdb.theme.Theme.decode(id) for id in dict_inst.get("themes", [])]
        game_inst._platforms = [vgmdb.platform.Platform.decode(id) for id in dict_inst.get("platforms", [])]
        #game_inst._themes = dict_inst.get("themes", [])
        return game_inst

    