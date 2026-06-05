# Диаграмма 16. C4 Containers: после реструктуризации (рисунок 16)

## Назначение
Рисунок 16 отчёта ПР8. C4 Container diagram **ASTROLL** (сервисная архитектура).

## Эталон (что должно получиться)
- Как MDT рис. 16: **несколько Django/FastAPI сервисов** за **API Gateway**.
- **Frontend [React]**, **PostgreSQL**, **Redis Cache**, **Broker**, **Object Storage**.
- **Session Service [Django/DRF + worker]** содержит API и внутренний realtime-worker.
- **Нет ML-service** — вместо него **Board Service** и асинхронный контур внутри **Session Service**.
- Все сервисы из `ASTROLL/services/*`.

## Промпт для генерации
```
Нарисуй C4 Container Diagram ASTROLL ПОСЛЕ реструктуризации (рис. 16 MDT).

Persons: Игрок, Мастер, Администратор → API Gateway.

Containers:
- API Gateway [Nginx]
- Frontend [React]
- Identity Service [Django/DRF] — auth, accounts, friends
- Character Service [Django/DRF]
- Session Service [Django/DRF] — комнаты, команды, права
- Board Service [Django/DRF] — снапшоты, элементы
- Dice Service [Django/DRF]
- Administration Service [Django/DRF]
- Database [PostgreSQL] — логически общая, сервисы используют свои схемы
- Cache [Redis] — presence, кеш
- Broker [RabbitMQ/Redis Streams]
- Object Storage [MinIO]

Связи:
Gateway → все сервисы + Frontend
Frontend → Session (WebSocket) через Gateway
Session API → Broker → Session internal worker
Board, Session → Object Storage
Identity ← Characters, Session, Board, Dice, Administration (JWT)
All services → Database
Session internal worker → Broker, Cache, Board, Storage

Показать независимое масштабирование Session и Board. Подписать: «6 сервисов; realtime-worker — внутренний компонент Session Service».
```

## PlantUML (готовая реализация)
```plantuml
@startuml
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Container.puml

LAYOUT_TOP_DOWN()

Person(player, "Игрок", "Играет в комнате")
Person(master, "Мастер", "Ведёт сессию")
Person(admin, "Администратор", "Эксплуатация")

System_Boundary(astroll, "ASTROLL после реструктуризации") {
  Container(gateway, "API Gateway", "Nginx", "Маршрутизация, TLS,\nrate limiting")
  Container(frontend, "Frontend", "React", "UI VTT")
  Container(identity, "Identity Service", "Django/DRF", "JWT, профиль, друзья,\nпоиск, RBAC")
  Container(characters, "Character Service", "Django/DRF", "Персонажи, листы")
  Container(session, "Session Service", "Django/DRF + worker", "Комнаты, команды,\nSessionPolicy, WSS broadcast")
  Container(board, "Board Service", "Django/DRF", "Снапшоты, элементы,\nExcalidrawAdapter")
  Container(dice, "Dice Service", "Django/DRF", "Броски, история")
  Container(adminSvc, "Administration Service", "Django/DRF", "Runtime-настройки")
  ContainerDb(db, "Database", "PostgreSQL", "Транзакционные данные")
  ContainerDb(cache, "Cache", "Redis", "Presence, кеш")
  ContainerQueue(broker, "Broker", "Redis Streams", "SessionEventDTO")
  ContainerDb(storage, "Object Storage", "MinIO", "Карты, портреты")
}

Rel(player, gateway, "HTTPS / WSS")
Rel(master, gateway, "HTTPS / WSS")
Rel(admin, gateway, "HTTPS")
Rel(gateway, frontend, "static")
Rel(gateway, identity, "REST")
Rel(gateway, characters, "REST")
Rel(gateway, session, "REST / WSS")
Rel(gateway, board, "REST")
Rel(gateway, dice, "REST")
Rel(gateway, adminSvc, "REST")
Rel(frontend, session, "WebSocket", "sync")
Rel(session, broker, "publish events")
Rel(broker, session, "consume by internal worker")
Rel(session, cache, "presence")
Rel(board, storage, "S3")
Rel(characters, storage, "S3")
Rel(characters, identity, "owner check")
Rel(session, identity, "JWT")
Rel(board, identity, "JWT")
Rel(dice, identity, "JWT")
Rel(adminSvc, identity, "RBAC")
Rel(identity, db, "SQL")
Rel(characters, db, "SQL")
Rel(session, db, "SQL")
Rel(board, db, "SQL")
Rel(dice, db, "SQL")
Rel(adminSvc, db, "SQL")
Rel(session, storage, "S3 snapshots")
@enduml
```
