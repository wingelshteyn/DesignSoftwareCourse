# Диаграмма 10. SOLID: DIP для журналирования команд

## Промпт
Создай UML/C4 Code диаграмму для принципа инверсии зависимостей в ASTROLL. Высокоуровневый GameSessionCommandInvoker не должен зависеть от конкретного журнала в базе или от WebSocket-публикатора. Он зависит от интерфейсов SessionEventLog и RealtimeEventPublisher. Конкретные классы DatabaseSessionEventLog, NullSessionEventLog и SocketIoEventPublisher реализуют эти интерфейсы.

## PlantUML
```plantuml
@startuml
skinparam classAttributeIconSize 0

class GameSessionCommandInvoker {
  -event_log: SessionEventLog
  -publisher: RealtimeEventPublisher
  +execute(command: GameSessionCommand): SessionEvent
}

abstract class GameSessionCommand {
  +execute(): SessionEvent
}

interface SessionEventLog {
  +append(event: SessionEvent): void
}

class DatabaseSessionEventLog {
  -repository: EventRepository
  +append(event: SessionEvent): void
}

class NullSessionEventLog {
  +append(event: SessionEvent): void
}

interface RealtimeEventPublisher {
  +publish(room_id: str, event: SessionEvent): void
}

class SocketIoEventPublisher {
  -server: SocketServer
  +publish(room_id: str, event: SessionEvent): void
}

class SessionEvent {
  +room_id: str
  +type: str
  +payload: dict
}

GameSessionCommandInvoker --> GameSessionCommand
GameSessionCommandInvoker o-- SessionEventLog
GameSessionCommandInvoker o-- RealtimeEventPublisher
SessionEventLog <|.. DatabaseSessionEventLog
SessionEventLog <|.. NullSessionEventLog
RealtimeEventPublisher <|.. SocketIoEventPublisher
GameSessionCommand ..> SessionEvent
DatabaseSessionEventLog --> EventRepository

note bottom of GameSessionCommandInvoker
DIP: invoker зависит от абстракций,
а инфраструктура подставляется снаружи.
end note
@enduml
```
