# Диаграмма 15. C4 Containers до реструктуризации

## Промпт
Создай C4 Container диаграмму ASTROLL до реструктуризации. Архитектура: сервисная архитектура с модульным backend-монолитом. Контейнеры: API Gateway, Frontend React, Backend Django/DRF с модулями Accounts, Friends, Characters, Rooms, Board, Dice, Game Session, PostgreSQL, Redis, Object Storage, Worker. Покажи, что весь доменный функционал находится в одном backend-контейнере, поэтому масштабируется целиком.

## PlantUML
```plantuml
@startuml
left to right direction
skinparam componentStyle rectangle

actor "Игрок" as Player
actor "Мастер" as Master

node "ASTROLL до реструктуризации" {
  component "API Gateway\n[Nginx]" as Gateway
  component "Frontend\n[React]" as Frontend
  component "Backend\n[Django/DRF]\nмодульный монолит:\nAccounts, Friends,\nCharacters, Rooms,\nBoard, Dice, Game Session" as Backend
  component "Worker\n[Celery]" as Worker
  database "Database\n[PostgreSQL]" as DB
  database "Cache/Broker\n[Redis]" as Redis
  database "Object Storage\n[MinIO]" as Storage
}

Player --> Gateway
Master --> Gateway
Gateway --> Frontend
Gateway --> Backend : REST/WebSocket
Frontend --> Backend
Backend --> DB
Backend --> Redis
Backend --> Storage
Backend --> Worker
Worker --> Redis
Worker --> DB
Worker --> Storage

note bottom of Backend
Один backend-контейнер содержит
все бизнес-модули и масштабируется целиком.
end note
@enduml
```
