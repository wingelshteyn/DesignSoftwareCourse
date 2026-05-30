from dataclasses import dataclass

from astroll_shared_contracts import BoardSnapshotDTO, SessionEventDTO


@dataclass(frozen=True)
class BrokerMessage:
    routing_key: str
    payload: dict


class RealtimeGateway:
    def publish_to_room(self, event: SessionEventDTO) -> BrokerMessage:
        return BrokerMessage(
            routing_key=f"room.{event.room_id}.{event.event_type}",
            payload={"room_id": event.room_id, "event_type": event.event_type, "payload": event.payload},
        )


class SnapshotPersistenceWorker:
    def persist_snapshot(self, snapshot: BoardSnapshotDTO) -> BrokerMessage:
        return BrokerMessage(
            routing_key=f"board.{snapshot.board_id}.snapshot.persisted",
            payload={"board_id": snapshot.board_id, "room_id": snapshot.room_id, "version": snapshot.version},
        )
