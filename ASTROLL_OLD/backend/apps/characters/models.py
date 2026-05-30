from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class CharacterSheet:
    schema_version: int
    data: dict[str, Any]
    updated_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Character:
    character_id: int
    owner_id: int
    name: str
    sheet: CharacterSheet


class CharacterAccessPolicy:
    def can_read(self, user_id: int, character: Character) -> bool:
        return character.owner_id == user_id

    def can_update(self, user_id: int, character: Character) -> bool:
        return character.owner_id == user_id
