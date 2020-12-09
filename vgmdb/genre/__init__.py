from __future__ import annotations
from vgmdb.databaseobj import DatabaseObject

GENREDATA = []
import json
with open("vgmdb/data/genres.json", "r") as f:
    GENREDATA = json.load(f)

class Genre(DatabaseObject):
    def __init__(self, id: int):
        super().__init__(id)
        self.name = ""

        for genre_info in GENREDATA:
            if genre_info["id"] == id:
                self.name = genre_info["name"]
                break
        else:
            raise Exception("Invalid genre id {}.".format(id))

    def __eq__(self, other: Genre) -> bool:
        return self.id == other.id

    def encode(self) -> int:
        return self.id
    
    @classmethod
    def decode(cls, genre_id: int) -> Genre:
        return cls(genre_id)