from random import randint

from astroll_shared_contracts import DiceRollDTO


class DiceApplicationService:
    def roll_d20(self, room_id: str, author_id: int, modifier: int = 0) -> DiceRollDTO:
        return DiceRollDTO(
            room_id=room_id,
            author_id=author_id,
            formula=f"1d20+{modifier}",
            total=randint(1, 20) + modifier,
        )
