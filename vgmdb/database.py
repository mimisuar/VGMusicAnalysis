from __future__ import annotations
import vgmdb.game

class Database:
    def __init__(self):
        self.games = []

    def add_game(self, game: vgmdb.game.Game) -> None:
        if game not in self.games:
            self.games.append(game)

    def encode(self) -> list:
        return [game.encode() for game in self.games]

    @classmethod
    def decode(cls, list_inst: list) -> Database:
        assert isinstance(list_inst, list), "Database decode only works on lists."
        db = Database()
        db.games = [vgmdb.game.Game.decode(obj) for obj in list_inst]