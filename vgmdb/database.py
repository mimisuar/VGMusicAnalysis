from __future__ import annotations
from typing import Generator
import vgmdb.game

DEFAULT_DATABASE = "vgmdb/data/games.json"

class Database:
    def __init__(self):
        self.games = []

    def add_game(self, game: vgmdb.game.Game) -> None:
        if game not in self.games:
            self.games.append(game)

    def get_games(self) -> Generator[vgmdb.game.Game, None, None]:
        yield from self.games

    def encode(self) -> list:
        return [game.encode() for game in self.games]

    @classmethod
    def decode(cls, list_inst: list) -> Database:
        assert isinstance(list_inst, list), "Database decode only works on lists."
        db = Database()
        db.games = [vgmdb.game.Game.decode(obj) for obj in list_inst]
        return db

    @staticmethod
    def get_default_database() -> Database:
        import json
        with open(DEFAULT_DATABASE, "r") as f:
            tmp = json.load(f)
        return Database.decode(tmp)