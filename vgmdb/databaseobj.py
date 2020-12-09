from __future__ import annotations

class DatabaseObject:
    def __init__(self, id: int):
        self.id = id

    def __eq__(self, other: DatabaseObject) -> bool:
        return self.id == other.id