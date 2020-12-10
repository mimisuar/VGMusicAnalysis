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
                if theme_info["id"] == self.id:
                    self._name = theme_info["name"]
                    break
            else:
                raise Exception("Invalid theme id {}.".format(self.id))
        return self._name

    def __repr__(self) -> str:
        return "Theme {0} (id:{1})".format(self.name, self.id)
    
    def encode(self) -> int:
        return self.id
    
    @classmethod
    def decode(cls, theme_id: int) -> Theme:
        return cls(theme_id)
