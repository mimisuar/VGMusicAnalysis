from __future__ import annotations
from vgmdb.databaseobj import DatabaseObject

PLATFORMDATA = []
import json
with open("vgmdb/data/platforms.json", "r") as f:
    PLATFORMDATA = json.load(f)

PLATFORMCATS = [
    "console",
    "arcade",
    "platform",
    "operating_system",
    "portable_console",
    "computer",
]

class Platform(DatabaseObject):
    def __init__(self, id: int):
        super().__init__(id)
        self._cat = -1
        self._abbr = None
        self._name = None

    @property
    def name(self) -> str:
        if not self._name:
            for pform_info in PLATFORMDATA:
                if pform_info["id"] == id:
                    self.name = pform_info.get("name", "")
                    break
            else:
                raise Exception("Invalid platform id \"{}\".".format(id))
        return self.name

    @property
    def abbr(self) -> str:
        if not self._abbr:
            for pform_info in PLATFORMDATA:
                if pform_info["id"] == id:
                    self.abbr = pform_info.get("abbreviation", "")
                    break
            else:
                raise Exception("Invalid platform id \"{}\".".format(id))
        return self._abbr

    @property
    def category(self):
        if self._cat == -1:
            for pform_info in PLATFORMDATA:
                if pform_info["id"] == id:
                    self._cat = pform_info.get("category", 0)
                    break
            else:
                raise Exception("Invalid platform id \"{}\".".format(id))
        
        if 0 <= self._cat < len(PLATFORMCATS):
            return PLATFORMCATS[self._cat]
        raise IndexError("Category is out of index!")

    def encode(self) -> int:
        return self.id
    
    @classmethod
    def decode(cls, platform_id: int) -> Platform:
        return cls(platform_id)
    
    @classmethod
    def get_platform_by_abbr(cls, target_abbr: str) -> Platform:
        for pform_info in PLATFORMDATA:
            if pform_info.get("abbreviation", "").lower() == target_abbr.lower():
                return Platform(pform_info["id"])
        raise Exception("Failed to find platform with abbreviation {}.".format(target_abbr))