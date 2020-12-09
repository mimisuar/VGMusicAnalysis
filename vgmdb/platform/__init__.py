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
        self.name = ""
        self.abbr = ""
        self.category_id = 0

        for pform_info in PLATFORMDATA:
            if pform_info["id"] == id:
                self.name = pform_info.get("name", "")
                self.abbr = pform_info.get("abbreviation", "")
                self.categroy_id = pform_info.get("category", 0)
                break
        else:
            raise Exception("Invalid platform id \"{}\".".format(id))

    @property
    def category(self):
        if 0 <= self.category_id < len(PLATFORMCATS):
            return PLATFORMCATS[self.category_id]
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