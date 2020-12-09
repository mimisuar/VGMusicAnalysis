from __future__ import annotations
from os import name
from vgmdb.databaseobj import DatabaseObject

THEMEDATA = []
import json
with open("vgmdb/data/themes.json", "r") as f:
    THEMEDATA = json.load(f)

class Theme(DatabaseObject):
    def __init__(self, id: int):
        super().__init__(id)
        self._name = None
        
    @property
    def name(self) -> str:
        if not self._name:
            for theme_info in THEMEDATA:
                if theme_info["id"] == id:
                    self._name = theme_info["name"]
                    break
            else:
                raise Exception("Invalid theme id {}.".format(id))
        return self._name

    
    def encode(self) -> int:
        return self.id
    
    @classmethod
    def decode(cls, theme_id: int) -> Theme:
        return cls(theme_id)
