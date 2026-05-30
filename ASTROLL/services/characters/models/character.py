from dataclasses import dataclass
from typing import Any

from astroll_shared_contracts import CharacterRef


@dataclass
class CharacterSheet:
    schema_version: int
    data: dict[str, Any]


@dataclass
class Character:
    character_id: int
    owner_id: int
    name: str
    sheet: CharacterSheet

    def to_ref(self) -> CharacterRef:
        return CharacterRef(self.character_id, self.owner_id, self.name)
