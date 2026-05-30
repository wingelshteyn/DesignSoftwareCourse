from dataclasses import dataclass, field
from typing import Any

from astroll_shared_contracts import BoardElementDTO, BoardSnapshotDTO


@dataclass
class ExcalidrawJson:
    elements: list[dict[str, Any]]
    app_state: dict[str, Any] = field(default_factory=dict)
    files: dict[str, Any] = field(default_factory=dict)


class ExcalidrawSnapshotAdapter:
    """ACL that prevents Excalidraw JSON from leaking into other services."""

    def to_contract(self, board_id: int, room_id: str, json: ExcalidrawJson) -> BoardSnapshotDTO:
        elements = [
            BoardElementDTO(
                element_id=str(raw["id"]),
                element_type=str(raw["type"]),
                payload=dict(raw),
            )
            for raw in json.elements
        ]
        return BoardSnapshotDTO(board_id=board_id, room_id=room_id, version=1, elements=elements)

    def to_excalidraw(self, snapshot: BoardSnapshotDTO) -> ExcalidrawJson:
        return ExcalidrawJson(elements=[{"id": e.element_id, "type": e.element_type, **e.payload} for e in snapshot.elements])
