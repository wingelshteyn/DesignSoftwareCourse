from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class UserRef:
    user_id: int
    nickname: str


@dataclass(frozen=True)
class CharacterRef:
    character_id: int
    owner_id: int
    name: str


@dataclass(frozen=True)
class RoomRef:
    room_id: str
    host_id: int


@dataclass(frozen=True)
class BoardElementDTO:
    element_id: str
    element_type: str
    payload: dict[str, Any]


@dataclass(frozen=True)
class BoardSnapshotDTO:
    board_id: int
    room_id: str
    version: int
    elements: list[BoardElementDTO]


@dataclass(frozen=True)
class DiceRollDTO:
    room_id: str
    author_id: int
    formula: str
    total: int


@dataclass(frozen=True)
class SessionEventDTO:
    room_id: str
    event_type: str
    payload: dict[str, Any]
