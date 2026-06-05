# Диаграмма 18. 4+1: процессное представление (рисунок 18)

## Назначение
Рисунок 18 отчёта ПР8. **Process View** — потоки синхронных и асинхронных запросов.

## Эталон (что должно получиться)
- **API Gateway** сверху по центру.
- Пунктирная граница **[Session Process]** вокруг Session API, Broker, Session Realtime Worker, Board Service.
- **Двойные стрелки** (HTTP sync) от Gateway к сервисам.
- **Пунктирные стрелки** (async) Session API → Broker → Session Realtime Worker.
- Параллелограммы/прямоугольники как в MDT process diagram.
- Сценарий: игрок двигает токен → broadcast всем клиентам.

## Промпт для генерации
```
Нарисуй Process View (4+1) для ASTROLL, стиль рис. 18 MDT (процессная диаграмма).

Элементы:
- API Gateway (верх, центр) — три маленьких прямоугольника слева = endpoints
- Other Services (справа вне процесса) — Identity, Characters
- Пунктирная рамка [Session Process]:
  - Session API (принимает команды комнаты)
  - Broker [Redis Streams]
  - Session Realtime Worker (внутренний worker-компонент Session Service, WebSocket broadcast)
  - Board Service (валидация элементов, опционально)

Потоки:
1. Клиент → API Gateway → Session API (sync, двойная линия) — POST /rooms/{id}/commands
2. Session API → Broker (solid) — publish SessionEventDTO
3. Broker → Session Realtime Worker (dashed async)
4. Session Realtime Worker → Клиенты (broadcast)
5. Session API → Board Service (sync, optional validate)

Подпись сценария: «MoveTokenCommand → SessionEvent → Redis → Session Realtime Worker → WebSocket».
```

## PlantUML (готовая реализация)
```plantuml
@startuml
skinparam rectangle {
  BackgroundColor white
  BorderColor black
}
skinparam componentStyle rectangle
skinparam arrowThickness 2

rectangle "API Gateway" as GW {
  rectangle " " as ep1
  rectangle " " as ep2
  rectangle " " as ep3
}

rectangle "Identity & Character\nServices" as Other

together {
  rectangle "Session Process" as SP #white;line:dashed;text:[Session Process] {
    rectangle "Session API" as Session
    rectangle "Broker\n[Redis Streams]" as Broker
    rectangle "Session Realtime\nWorker" as Worker
    rectangle "Board Service" as Board
  }
}

actor "Клиент\n(Игрок/Мастер)" as Client

Client -[#black,bold]-> GW : HTTPS
GW -[#black,bold]-> Session : POST /rooms/{id}/commands
GW -[#black,bold]-> Other : REST
Session -[#black]-> Broker : publish\nSessionEventDTO
Broker ..[#black,dashed]-> Worker : consume
Worker ..[#black,dashed]-> Client : WebSocket\nbroadcast
Session -[#black,bold]-> Board : validate element\n(optional)

note bottom of Session
  MoveTokenCommand →
  SessionPolicy → execute →
  SessionEventDTO
end note
@enduml
```
