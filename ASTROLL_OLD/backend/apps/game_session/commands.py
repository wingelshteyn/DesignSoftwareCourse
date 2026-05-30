from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

from apps.board.adapters import BoardSnapshot, BoardSnapshotProvider
from apps.board.elements import BoardActionPayload, BoardElement, BoardUpdateBuilder
from apps.dice.models import DiceRollEntry, DiceRoller
from apps.rooms.models import Room


@dataclass(frozen=True)
class SessionEvent:
    room_id: str
    event_type: str
    payload: dict[str, Any]


@dataclass
class GameSession:
    room: Room
    board: BoardSnapshot
    dice_roller: DiceRoller
    elements: list[BoardElement] = field(default_factory=list)
    rolls: list[DiceRollEntry] = field(default_factory=list)

    def add_element(self, element: BoardElement) -> SessionEvent:
        self.elements.append(element)
        return SessionEvent(self.room.room_id, "board.element_added", element.to_snapshot())

    def move_token(self, token_id: str, x: float, y: float) -> SessionEvent:
        return SessionEvent(self.room.room_id, "board.token_moved", {"token_id": token_id, "x": x, "y": y})

    def roll_dice(self, author_id: int, modifier: int = 0) -> SessionEvent:
        entry = self.dice_roller.roll_d20(self.room.room_id, author_id, modifier)
        self.rolls.append(entry)
        return SessionEvent(self.room.room_id, "dice.rolled", entry.__dict__)

    def set_readonly(self, target_user_id: int, readonly: bool) -> SessionEvent:
        self.room.set_readonly(target_user_id, readonly)
        return SessionEvent(self.room.room_id, "room.readonly_changed", {"user_id": target_user_id, "readonly": readonly})

    def kick(self, target_user_id: int) -> SessionEvent:
        self.room.members.pop(target_user_id, None)
        return SessionEvent(self.room.room_id, "room.member_kicked", {"user_id": target_user_id})


class GameSessionCommand(ABC):
    def __init__(self, session: GameSession, actor_id: int) -> None:
        self.session = session
        self.actor_id = actor_id

    @abstractmethod
    def execute(self) -> SessionEvent:
        raise NotImplementedError


class AddBoardElementCommand(GameSessionCommand):
    def __init__(self, session: GameSession, actor_id: int, payload: BoardActionPayload, builder: BoardUpdateBuilder) -> None:
        super().__init__(session, actor_id)
        self.payload = payload
        self.builder = builder

    def execute(self) -> SessionEvent:
        return self.session.add_element(self.builder.build(self.payload))


class MoveTokenCommand(GameSessionCommand):
    def __init__(self, session: GameSession, actor_id: int, token_id: str, x: float, y: float) -> None:
        super().__init__(session, actor_id)
        self.token_id = token_id
        self.x = x
        self.y = y

    def execute(self) -> SessionEvent:
        return self.session.move_token(self.token_id, self.x, self.y)


class RollDiceCommand(GameSessionCommand):
    def __init__(self, session: GameSession, actor_id: int, modifier: int = 0) -> None:
        super().__init__(session, actor_id)
        self.modifier = modifier

    def execute(self) -> SessionEvent:
        return self.session.roll_dice(self.actor_id, self.modifier)


class SetReadonlyCommand(GameSessionCommand):
    def __init__(self, session: GameSession, actor_id: int, target_user_id: int, readonly: bool) -> None:
        super().__init__(session, actor_id)
        self.target_user_id = target_user_id
        self.readonly = readonly

    def execute(self) -> SessionEvent:
        return self.session.set_readonly(self.target_user_id, self.readonly)


class KickPlayerCommand(GameSessionCommand):
    def __init__(self, session: GameSession, actor_id: int, target_user_id: int) -> None:
        super().__init__(session, actor_id)
        self.target_user_id = target_user_id

    def execute(self) -> SessionEvent:
        return self.session.kick(self.target_user_id)


class SaveBoardSnapshotCommand(GameSessionCommand):
    def __init__(self, session: GameSession, actor_id: int, provider: BoardSnapshotProvider) -> None:
        super().__init__(session, actor_id)
        self.provider = provider

    def execute(self) -> SessionEvent:
        self.provider.save_snapshot(self.session.board.board_id, self.session.board)
        return SessionEvent(self.session.room.room_id, "board.snapshot_saved", {"board_id": self.session.board.board_id})


class SessionPolicy:
    def can_execute(self, actor_id: int, command: GameSessionCommand) -> bool:
        if isinstance(command, (SetReadonlyCommand, KickPlayerCommand)):
            return command.session.room.is_host(actor_id)
        member = command.session.room.members.get(actor_id)
        return member is not None and not member.readonly


class SessionEventLog(ABC):
    @abstractmethod
    def append(self, event: SessionEvent) -> None:
        raise NotImplementedError


class InMemorySessionEventLog(SessionEventLog):
    def __init__(self) -> None:
        self.events: list[SessionEvent] = []

    def append(self, event: SessionEvent) -> None:
        self.events.append(event)


class RealtimeEventPublisher(ABC):
    @abstractmethod
    def publish(self, room_id: str, event: SessionEvent) -> None:
        raise NotImplementedError


class NullRealtimeEventPublisher(RealtimeEventPublisher):
    def publish(self, room_id: str, event: SessionEvent) -> None:
        return None


class GameSessionCommandInvoker:
    def __init__(self, policy: SessionPolicy, event_log: SessionEventLog, publisher: RealtimeEventPublisher) -> None:
        self.policy = policy
        self.event_log = event_log
        self.publisher = publisher

    def execute(self, command: GameSessionCommand) -> SessionEvent:
        if not self.policy.can_execute(command.actor_id, command):
            raise PermissionError("actor cannot execute this session command")
        event = command.execute()
        self.event_log.append(event)
        self.publisher.publish(event.room_id, event)
        return event
