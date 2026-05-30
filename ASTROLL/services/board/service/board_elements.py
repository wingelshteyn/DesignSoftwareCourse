from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any
from uuid import uuid4

from astroll_shared_contracts import BoardElementDTO, BoardSnapshotDTO


@dataclass(frozen=True)
class BoardActionPayload:
    room_id: str
    author_id: int
    element_type: str
    payload: dict[str, Any]


class BoardElement(ABC):
    def __init__(self, element_id: str | None = None) -> None:
        self.element_id = element_id or str(uuid4())

    @abstractmethod
    def to_dto(self) -> BoardElementDTO:
        raise NotImplementedError


class TokenElement(BoardElement):
    def __init__(self, character_id: int, element_id: str | None = None) -> None:
        super().__init__(element_id)
        self.character_id = character_id

    def to_dto(self) -> BoardElementDTO:
        return BoardElementDTO(self.element_id, "token", {"character_id": self.character_id})


class ImageElement(BoardElement):
    def __init__(self, image_url: str, element_id: str | None = None) -> None:
        super().__init__(element_id)
        self.image_url = image_url

    def to_dto(self) -> BoardElementDTO:
        return BoardElementDTO(self.element_id, "image", {"image_url": self.image_url})


class BoardElementFactory(ABC):
    @abstractmethod
    def create(self, payload: BoardActionPayload) -> BoardElement:
        raise NotImplementedError


class TokenElementFactory(BoardElementFactory):
    def create(self, payload: BoardActionPayload) -> BoardElement:
        return TokenElement(payload.payload["character_id"])


class ImageElementFactory(BoardElementFactory):
    def create(self, payload: BoardActionPayload) -> BoardElement:
        return ImageElement(payload.payload["image_url"])


class BoardElementFactoryRegistry:
    def __init__(self) -> None:
        self._factories: dict[str, BoardElementFactory] = {
            "token": TokenElementFactory(),
            "image": ImageElementFactory(),
        }

    def get(self, element_type: str) -> BoardElementFactory:
        return self._factories[element_type]


class BoardApplicationService:
    def __init__(self, registry: BoardElementFactoryRegistry | None = None) -> None:
        self._registry = registry or BoardElementFactoryRegistry()

    def create_element(self, payload: BoardActionPayload) -> BoardElementDTO:
        return self._registry.get(payload.element_type).create(payload).to_dto()

    def build_snapshot(self, board_id: int, room_id: str, elements: list[BoardElementDTO]) -> BoardSnapshotDTO:
        return BoardSnapshotDTO(board_id=board_id, room_id=room_id, version=1, elements=elements)
