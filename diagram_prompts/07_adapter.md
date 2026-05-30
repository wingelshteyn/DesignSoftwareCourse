# Диаграмма 7. Структурный паттерн: Адаптер

## Промпт
Создай UML class diagram для паттерна "Адаптер" в ASTROLL. Внутренний сервис GameSessionApplicationService работает с интерфейсом BoardSnapshotProvider. Сторонний формат ExcalidrawClient возвращает и принимает ExcalidrawJson. ExcalidrawSnapshotAdapter преобразует внешний JSON в доменные BoardSnapshot, BoardElement и обратно. Покажи, что адаптер реализует порт ядра и содержит ссылку на adaptee.

## PlantUML
```plantuml
@startuml
skinparam classAttributeIconSize 0

interface BoardSnapshotProvider {
  +load_snapshot(board_id: int): BoardSnapshot
  +save_snapshot(board_id: int, snapshot: BoardSnapshot): void
}

class GameSessionApplicationService {
  -snapshot_provider: BoardSnapshotProvider
  +open_board(room_id: str, board_id: int): BoardSnapshot
  +persist_board(room_id: str, snapshot: BoardSnapshot): void
}

class BoardSnapshot {
  +board_id: int
  +version: int
  +elements: list[BoardElement]
}

class BoardElement {
  +id: str
  +type: str
  +to_domain_event(): BoardEvent
}

class ExcalidrawClient {
  +read_scene(board_id: int): ExcalidrawJson
  +write_scene(board_id: int, json: ExcalidrawJson): void
}

class ExcalidrawJson {
  +elements: list[dict]
  +app_state: dict
  +files: dict
}

class ExcalidrawSnapshotAdapter {
  -adaptee: ExcalidrawClient
  +load_snapshot(board_id: int): BoardSnapshot
  +save_snapshot(board_id: int, snapshot: BoardSnapshot): void
  -to_domain(json: ExcalidrawJson): BoardSnapshot
  -to_excalidraw(snapshot: BoardSnapshot): ExcalidrawJson
}

ExcalidrawSnapshotAdapter ..|> BoardSnapshotProvider
ExcalidrawSnapshotAdapter o-- ExcalidrawClient : adaptee
GameSessionApplicationService o-- BoardSnapshotProvider
BoardSnapshot o-- BoardElement
ExcalidrawClient ..> ExcalidrawJson
ExcalidrawSnapshotAdapter ..> BoardSnapshot
ExcalidrawSnapshotAdapter ..> ExcalidrawJson
@enduml
```
