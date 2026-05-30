from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

from apps.board.elements import BoardActionPayload, BoardElement, BoardUpdateBuilder, default_element_registry


@dataclass
class BoardSnapshot:
    board_id: int
    version: int
    elements: list[BoardElement] = field(default_factory=list)


@dataclass
class ExcalidrawJson:
    elements: list[dict[str, Any]]
    app_state: dict[str, Any] = field(default_factory=dict)
    files: dict[str, Any] = field(default_factory=dict)


class BoardSnapshotProvider(ABC):
    @abstractmethod
    def load_snapshot(self, board_id: int) -> BoardSnapshot:
        raise NotImplementedError

    @abstractmethod
    def save_snapshot(self, board_id: int, snapshot: BoardSnapshot) -> None:
        raise NotImplementedError


class ExcalidrawClient:
    def __init__(self) -> None:
        self._storage: dict[int, ExcalidrawJson] = {}

    def read_scene(self, board_id: int) -> ExcalidrawJson:
        return self._storage.get(board_id, ExcalidrawJson(elements=[]))

    def write_scene(self, board_id: int, json: ExcalidrawJson) -> None:
        self._storage[board_id] = json


class ExcalidrawSnapshotAdapter(BoardSnapshotProvider):
    """Anti-corruption layer between ASTROLL domain snapshots and Excalidraw JSON."""

    def __init__(self, adaptee: ExcalidrawClient) -> None:
        self._adaptee = adaptee

    def load_snapshot(self, board_id: int) -> BoardSnapshot:
        return self._to_domain(board_id, self._adaptee.read_scene(board_id))

    def save_snapshot(self, board_id: int, snapshot: BoardSnapshot) -> None:
        self._adaptee.write_scene(board_id, self._to_excalidraw(snapshot))

    def _to_domain(self, board_id: int, json: ExcalidrawJson) -> BoardSnapshot:
        builder = BoardUpdateBuilder(default_element_registry())
        elements = []
        for raw in json.elements:
            payload = BoardActionPayload(
                room_id=raw.get("room_id", "unknown"),
                author_id=raw.get("created_by", 0),
                element_type=raw["type"],
                data=raw,
            )
            elements.append(builder.build(payload))
        return BoardSnapshot(board_id=board_id, version=1, elements=elements)

    def _to_excalidraw(self, snapshot: BoardSnapshot) -> ExcalidrawJson:
        return ExcalidrawJson(elements=[element.to_snapshot() for element in snapshot.elements])
