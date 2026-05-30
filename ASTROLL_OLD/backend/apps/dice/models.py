from dataclasses import dataclass
from random import randint


@dataclass(frozen=True)
class DiceRollEntry:
    room_id: str
    author_id: int
    formula: str
    total: int
    description: str


class DiceRoller:
    def roll_d20(self, room_id: str, author_id: int, modifier: int = 0) -> DiceRollEntry:
        value = randint(1, 20) + modifier
        return DiceRollEntry(room_id, author_id, f"1d20+{modifier}", value, "D20 check")
