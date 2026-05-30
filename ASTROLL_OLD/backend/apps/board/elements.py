from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4


@dataclass(frozen=True)
class Point:
    x: float
    y: float


@dataclass
class BoardActionPayload:
    room_id: str
    author_id: int
    element_type: str
    data: dict[str, Any]


@dataclass
class BoardElement(ABC):
    room_id: str
    created_by: int
    position: Point
    element_id: str = field(default_factory=lambda: str(uuid4()))

    def can_edit(self, user_id: int) -> bool:
        return self.created_by == user_id

    @abstractmethod
    def to_snapshot(self) -> dict[str, Any]:
        raise NotImplementedError


@dataclass
class TokenElement(BoardElement):
    character_id: int = 0

    def to_snapshot(self) -> dict[str, Any]:
        return {"type": "token", "id": self.element_id, "character_id": self.character_id}


@dataclass
class ImageElement(BoardElement):
    image_url: str = ""

    def to_snapshot(self) -> dict[str, Any]:
        return {"type": "image", "id": self.element_id, "image_url": self.image_url}


@dataclass
class TextElement(BoardElement):
    text: str = ""

    def to_snapshot(self) -> dict[str, Any]:
        return {"type": "text", "id": self.element_id, "text": self.text}


@dataclass
class ShapeElement(BoardElement):
    shape_type: str = "rectangle"

    def to_snapshot(self) -> dict[str, Any]:
        return {"type": "shape", "id": self.element_id, "shape_type": self.shape_type}


@dataclass
class DrawingElement(BoardElement):
    points: list[Point] = field(default_factory=list)

    def to_snapshot(self) -> dict[str, Any]:
        return {"type": "drawing", "id": self.element_id, "points": [p.__dict__ for p in self.points]}


class BoardElementFactory(ABC):
    @abstractmethod
    def create_element(self, payload: BoardActionPayload) -> BoardElement:
        raise NotImplementedError


class TokenElementFactory(BoardElementFactory):
    def create_element(self, payload: BoardActionPayload) -> BoardElement:
        return TokenElement(payload.room_id, payload.author_id, Point(**payload.data["position"]), payload.data.get("id", str(uuid4())), payload.data["character_id"])


class ImageElementFactory(BoardElementFactory):
    def create_element(self, payload: BoardActionPayload) -> BoardElement:
        return ImageElement(payload.room_id, payload.author_id, Point(**payload.data["position"]), payload.data.get("id", str(uuid4())), payload.data["image_url"])


class TextElementFactory(BoardElementFactory):
    def create_element(self, payload: BoardActionPayload) -> BoardElement:
        return TextElement(payload.room_id, payload.author_id, Point(**payload.data["position"]), payload.data.get("id", str(uuid4())), payload.data["text"])


class ShapeElementFactory(BoardElementFactory):
    def create_element(self, payload: BoardActionPayload) -> BoardElement:
        return ShapeElement(payload.room_id, payload.author_id, Point(**payload.data["position"]), payload.data.get("id", str(uuid4())), payload.data.get("shape_type", "rectangle"))


class DrawingElementFactory(BoardElementFactory):
    def create_element(self, payload: BoardActionPayload) -> BoardElement:
        points = [Point(**point) for point in payload.data.get("points", [])]
        return DrawingElement(payload.room_id, payload.author_id, Point(**payload.data["position"]), payload.data.get("id", str(uuid4())), points)


class BoardElementFactoryRegistry:
    def __init__(self) -> None:
        self._factories: dict[str, BoardElementFactory] = {}

    def register(self, element_type: str, factory: BoardElementFactory) -> None:
        self._factories[element_type] = factory

    def get_factory(self, element_type: str) -> BoardElementFactory:
        return self._factories[element_type]


class BoardUpdateBuilder:
    def __init__(self, registry: BoardElementFactoryRegistry) -> None:
        self._registry = registry

    def build(self, payload: BoardActionPayload) -> BoardElement:
        return self._registry.get_factory(payload.element_type).create_element(payload)


def default_element_registry() -> BoardElementFactoryRegistry:
    registry = BoardElementFactoryRegistry()
    registry.register("token", TokenElementFactory())
    registry.register("image", ImageElementFactory())
    registry.register("text", TextElementFactory())
    registry.register("shape", ShapeElementFactory())
    registry.register("drawing", DrawingElementFactory())
    return registry
