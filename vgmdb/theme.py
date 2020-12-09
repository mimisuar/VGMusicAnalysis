from __future__ import annotations

THEMEDATA = []
import json
with open("vgmdb/data/themes.json", "r") as f:
    THEMEDATA = json.load(f)

class Theme:
    def __init__(self, id):
        self.id = id
        self.name = ""

        for theme_info in THEMEDATA:
            if theme_info["id"] == id:
                self.name = theme_info["name"]
                break
        else:
            raise Exception("Invalid theme id {}.".format(self.id))
    
    def encode(self) -> int:
        return self.id
    
    @classmethod
    def decode(cls, theme_id: int) -> Theme:
        return cls(theme_id)
