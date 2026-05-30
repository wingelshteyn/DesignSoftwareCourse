# Диаграмма 10. SOLID: DIP (рисунок 10)

## Назначение
Рисунок 10 отчёта ПР8. UML с **инверсией зависимостей**: invoker зависит от абстракций лога и публикации.

## Эталон (что должно получиться)
- Как MDT рис. 10: **GameSessionCommandInvoker** → абстрактные **SessionEventLog**, **RealtimeEventPublisher**.
- **Null Object**: `NullSessionEventLog`, `NullRealtimeEventPublisher`.
- Конкретные: `InMemorySessionEventLog`, `SocketIoEventPublisher` (или `DatabaseSessionEventLog`).
- Жёлтые классы; invoker **не** зависит от конкретной БД или WebSocket.

## Промпт для генерации
```
Нарисуй UML Class Diagram для ASTROLL, демонстрирующий DIP (рис. 10 MDT).

GameSessionCommandInvoker (высокоуровневая политика) зависит от:
- abstract SessionEventLog (+append)
- abstract RealtimeEventPublisher (+publish)

Конкретные реализации:
- InMemorySessionEventLog implements SessionEventLog
- NullSessionEventLog implements SessionEventLog (Null Object)
- SocketIoEventPublisher implements RealtimeEventPublisher
- NullRealtimeEventPublisher implements RealtimeEventPublisher

Также GameSessionCommand (abstract) с execute(): SessionEvent.

Invoker НЕ зависит от InMemorySessionEventLog или SocketIo напрямую — только от интерфейсов.

Layout: Invoker слева, абстракции по центру, реализации справа/снизу. Жёлтые классы.
```

## PlantUML (готовая реализация)
```plantuml
@startuml
skinparam classAttributeIconSize 0
skinparam class {
  BackgroundColor #FEFECE
  BorderColor black
}

class GameSessionCommandInvoker {
  -event_log: SessionEventLog
  -publisher: RealtimeEventPublisher
  +execute(command: GameSessionCommand): SessionEvent
}

abstract class GameSessionCommand {
  +execute(): SessionEvent
}

abstract class SessionEventLog {
  +append(event: SessionEvent): void
}

class InMemorySessionEventLog {
  -events: list[SessionEvent]
  +append(event: SessionEvent): void
}

class NullSessionEventLog {
  +append(event: SessionEvent): void
}

abstract class RealtimeEventPublisher {
  +publish(room_id: str, event: SessionEvent): void
}

class SocketIoEventPublisher {
  -server: SocketServer
  +publish(room_id: str, event: SessionEvent): void
}

class NullRealtimeEventPublisher {
  +publish(room_id: str, event: SessionEvent): void
}

class SessionEvent {
  +room_id: str
  +event_type: str
  +payload: dict
}

GameSessionCommandInvoker --> GameSessionCommand
GameSessionCommandInvoker o-- SessionEventLog
GameSessionCommandInvoker o-- RealtimeEventPublisher

SessionEventLog <|-- InMemorySessionEventLog
SessionEventLog <|-- NullSessionEventLog
RealtimeEventPublisher <|-- SocketIoEventPublisher
RealtimeEventPublisher <|-- NullRealtimeEventPublisher

GameSessionCommand ..> SessionEvent

note bottom of GameSessionCommandInvoker
DIP: invoker зависит от абстракций;
инфраструктура подставляется снаружи.
end note
@enduml
```
