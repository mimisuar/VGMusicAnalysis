from __future__ import annotations

PLATFORMDATA = []
import json
with open("vgmdb/data/platforms.json", "r") as f:
    PLATFORMDATA = json.load(f)

PLATFORM_CATAGORY = [
    None,
    "console",
    "arcade",
    "platform",
    "operating_system",
    "portable_console",
    "computer",
]

class Platform:
    def __init__(self, id: int):
        self.id = id
        self.name = ""
        self.abbr = ""
        self.category = 0

        for pform_info in PLATFORMDATA:
            if pform_info["id"] == id:
                self.name = pform_info.get("name", "")
                self.abbr = pform_info.get("abbreviation", "")
                self.category = pform_info.get("category", 0)
                break
        else:
            raise Exception("Invalid platform id {}.".format(id))

    def encode(self) -> int:
        return self.id
    
    @classmethod
    def decode(cls, platform_id: int) -> Platform:
        return cls(platform_id)