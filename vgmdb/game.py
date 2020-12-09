from __future__ import annotations

class Game:
    def __init__(self) -> None:
        self._id = 0
        self._genres = []
        self._themes = []
        self._year = 0
        self._consoles = []
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

    def add_genre(self, genre_id: int) -> None:
        self._genres.append(genre_id)

    def add_theme(self, theme_id: int) -> None:
        self._themes.append(theme_id)

    def add_console(self, console_id: int) -> None:
        self._consoles.append(console_id)

    def encode(self) -> dict:
        return {
            "id": self._id,
            "name": self._name,
            "songs": self._songs,
            "genres": self._genres,
            "themes": self._themes,
            "consoles": self._consoles,
        }

    @classmethod
    def decode(cls, dict_inst: dict) -> Game:
        assert isinstance(dict_inst, dict), "Game decode only works on dictionarys."
        game_inst = cls()
        game_inst._id = dict_inst.get("id", 0)
        game_inst._name = dict_inst.get("name", "")
        game_inst._consoles = dict_inst.get("consoles", [])
        game_inst._genres = dict_inst.get("genres", [])
        game_inst._themes = dict_inst.get("themes", [])
        return game_inst

    