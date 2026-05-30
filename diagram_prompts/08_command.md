# Диаграмма 8. Поведенческий паттерн: Команда

## Промпт
Создай UML class diagram для паттерна "Команда" в ASTROLL. Действия в игровой комнате представлены командами: AddBoardElementCommand, MoveTokenCommand, RollDiceCommand, SetReadonlyCommand, KickPlayerCommand, SaveBoardSnapshotCommand. Все реализуют интерфейс GameSessionCommand. Получатель команд - GameSession. Invoker применяет команду, проверяет права через SessionPolicy, пишет событие в SessionEventLog и публикует его в realtime-шлюз.

## PlantUML
```plantuml
@startuml
skinparam classAttributeIconSize 0

abstract class GameSessionCommand {
  #session: GameSession
  #actor_id: int
  +execute(): SessionEvent
}

class AddBoardElementCommand { -payload: BoardActionPayload }
class MoveTokenCommand { -token_id: str; -position: Point }
class RollDiceCommand { -character_id: int; -formula: str }
class SetReadonlyCommand { -target_user_id: int; -readonly: bool }
class KickPlayerCommand { -target_user_id: int }
class SaveBoardSnapshotCommand { -board_name: str }

class GameSession {
  +room_id: str
  +members: list[RoomMember]
  +board: BoardSnapshot
  +add_element(element: BoardElement): void
  +move_token(token_id: str, position: Point): void
  +record_roll(entry: DiceRollEntry): void
  +set_readonly(user_id: int, readonly: bool): void
  +kick(user_id: int): void
  +save_snapshot(name: str): void
}

class GameSessionCommandInvoker {
  -policy: SessionPolicy
  -event_log: SessionEventLog
  -publisher: RealtimeEventPublisher
  +execute(command: GameSessionCommand): SessionEvent
}

interface SessionPolicy { +can_execute(actor_id: int, command: GameSessionCommand): bool }
interface SessionEventLog { +append(event: SessionEvent): void }
interface RealtimeEventPublisher { +publish(room_id: str, event: SessionEvent): void }
class SessionEvent { +room_id: str; +type: str; +payload: dict }

GameSessionCommand <|-- AddBoardElementCommand
GameSessionCommand <|-- MoveTokenCommand
GameSessionCommand <|-- RollDiceCommand
GameSessionCommand <|-- SetReadonlyCommand
GameSessionCommand <|-- KickPlayerCommand
GameSessionCommand <|-- SaveBoardSnapshotCommand
GameSessionCommand o-- GameSession
GameSessionCommandInvoker --> GameSessionCommand
GameSessionCommandInvoker --> SessionPolicy
GameSessionCommandInvoker --> SessionEventLog
GameSessionCommandInvoker --> RealtimeEventPublisher
GameSessionCommand ..> SessionEvent
@enduml
```
