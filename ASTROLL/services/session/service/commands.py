from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from astroll_shared_contracts import BoardElementDTO, DiceRollDTO, SessionEventDTO


@dataclass
class SessionState:
    room_id: str
    host_id: int
    members: dict[int, bool]
    elements: list[BoardElementDTO]
    rolls: list[DiceRollDTO]

    def is_host(self, user_id: int) -> bool:
        return self.host_id == user_id

    def is_readonly(self, user_id: int) -> bool:
        return self.members.get(user_id, True)


class GameSessionCommand(ABC):
    def __init__(self, state: SessionState, actor_id: int) -> None:
        self.state = state
        self.actor_id = actor_id

    @abstractmethod
    def execute(self) -> SessionEventDTO:
        raise NotImplementedError


class AddBoardElementCommand(GameSessionCommand):
    def __init__(self, state: SessionState, actor_id: int, element: BoardElementDTO) -> None:
        super().__init__(state, actor_id)
        self.element = element

    def execute(self) -> SessionEventDTO:
        self.state.elements.append(self.element)
        return SessionEventDTO(self.state.room_id, "board.element_added", self.element.__dict__)


class RollDiceCommand(GameSessionCommand):
    def __init__(self, state: SessionState, actor_id: int, roll: DiceRollDTO) -> None:
        super().__init__(state, actor_id)
        self.roll = roll

    def execute(self) -> SessionEventDTO:
        self.state.rolls.append(self.roll)
        return SessionEventDTO(self.state.room_id, "dice.rolled", self.roll.__dict__)


class SetReadonlyCommand(GameSessionCommand):
    def __init__(self, state: SessionState, actor_id: int, target_user_id: int, readonly: bool) -> None:
        super().__init__(state, actor_id)
        self.target_user_id = target_user_id
        self.readonly = readonly

    def execute(self) -> SessionEventDTO:
        self.state.members[self.target_user_id] = self.readonly
        return SessionEventDTO(self.state.room_id, "room.readonly_changed", {"user_id": self.target_user_id, "readonly": self.readonly})


class SessionPolicy:
    def can_execute(self, command: GameSessionCommand) -> bool:
        if isinstance(command, SetReadonlyCommand):
            return command.state.is_host(command.actor_id)
        return not command.state.is_readonly(command.actor_id)


class EventLog(ABC):
    @abstractmethod
    def append(self, event: SessionEventDTO) -> None:
        raise NotImplementedError


class EventPublisher(ABC):
    @abstractmethod
    def publish(self, event: SessionEventDTO) -> None:
        raise NotImplementedError


class SessionCommandInvoker:
    def __init__(self, policy: SessionPolicy, log: EventLog, publisher: EventPublisher) -> None:
        self._policy = policy
        self._log = log
        self._publisher = publisher

    def execute(self, command: GameSessionCommand) -> SessionEventDTO:
        if not self._policy.can_execute(command):
            raise PermissionError("command is not allowed")
        event = command.execute()
        self._log.append(event)
        self._publisher.publish(event)
        return event
