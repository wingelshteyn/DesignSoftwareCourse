# Диаграмма 16. C4 Containers после реструктуризации

## Промпт
Создай C4 Container диаграмму ASTROLL после реструктуризации под рост нагрузки. Раздели монолит на крупные сервисы: Auth & Accounts Service, Social Service, Character Service, Session Service, Board Service, Dice Service, Realtime Gateway, Administration Service. Добавь API Gateway, Frontend, PostgreSQL, Redis, Broker, Object Storage. Покажи, что Session/Realtime/Board можно масштабировать независимо, а асинхронные события проходят через Broker.

## PlantUML
```plantuml
@startuml
left to right direction
skinparam componentStyle rectangle

actor "Игрок" as Player
actor "Мастер" as Master
actor "Администратор" as Admin

node "ASTROLL после реструктуризации" {
  component "API Gateway\n[Nginx]" as Gateway
  component "Frontend\n[React]" as Frontend
  component "Realtime Gateway\n[Socket.IO]" as Realtime
  component "Auth & Accounts Service\n[Django/DRF]" as Auth
  component "Social Service\nдрузья, поиск" as Social
  component "Character Service\nлисты персонажей" as Characters
  component "Session Service\nкомнаты, права,\nкоманды сессии" as Session
  component "Board Service\nснапшоты,\nэлементы доски" as Board
  component "Dice Service\nброски и история" as Dice
  component "Administration Service\nнастройки, аудит" as AdminSvc
  database "Database\n[PostgreSQL]" as DB
  database "Cache\n[Redis]" as Cache
  queue "Broker\n[RabbitMQ/Redis Streams]" as Broker
  database "Object Storage\n[MinIO]" as Storage
}

Player --> Gateway
Master --> Gateway
Admin --> Gateway
Gateway --> Frontend
Gateway --> Auth
Gateway --> Social
Gateway --> Characters
Gateway --> Session
Gateway --> Board
Gateway --> Dice
Gateway --> AdminSvc
Gateway --> Realtime
Frontend --> Realtime
Realtime --> Session
Session --> Broker
Board --> Broker
Dice --> Broker
Characters --> Auth
Social --> Auth
Session --> Auth
Board --> Storage
Characters --> Storage
Auth --> DB
Social --> DB
Characters --> DB
Session --> DB
Board --> DB
Dice --> DB
AdminSvc --> DB
Realtime --> Cache
@enduml
```
