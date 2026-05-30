from dataclasses import dataclass


@dataclass(frozen=True)
class FriendLink:
    owner_id: int
    friend_id: int


class FriendPolicy:
    def can_add(self, owner_id: int, friend_id: int) -> bool:
        return owner_id != friend_id
