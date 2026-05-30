# Диаграмма 16. C4 Containers: после реструктуризации (рисунок 16)

## Назначение
Рисунок 16 отчёта ПР8. C4 Container diagram **ASTROLL** (сервисная архитектура).

## Эталон (что должно получиться)
- Как MDT рис. 16: **несколько Django/FastAPI сервисов** за **API Gateway**.
- **Frontend [React]**, **PostgreSQL**, **Redis Cache**, **Broker**, **Object Storage**.
- **Realtime Worker [Celery]** — асинхронный контур (аналог Control Worker).
- **Нет ML-service** — вместо него **Board Service** и **Realtime Worker**.
- Все сервисы из `ASTROLL/services/*`.

## Промпт для генерации
```
Нарисуй C4 Container Diagram ASTROLL ПОСЛЕ реструктуризации (рис. 16 MDT).

Persons: Игрок, Мастер, Администратор → API Gateway.

Containers:
- API Gateway [Nginx]
- Frontend [React]
- Auth & Accounts Service [Django/DRF]
- Social Service [Django/DRF] — friends
- Character Service [Django/DRF]
- Session Service [Django/DRF] — комнаты, команды, права
- Board Service [Django/DRF] — снапшоты, элементы
- Dice Service [Django/DRF]
- Administration Service [Django/DRF]
- Realtime Worker [Celery] — WebSocket broadcast, persist snapshots
- Database [PostgreSQL] — логически общая, сервисы используют свои схемы
- Cache [Redis] — presence, кеш
- Broker [RabbitMQ/Redis Streams]
- Object Storage [MinIO]

Связи:
Gateway → все сервисы + Frontend
Frontend → Realtime (WebSocket) через Gateway
Session → Broker → Realtime Worker
Board, Session → Object Storage
Auth ← Social, Characters, Session (JWT)
All services → Database
Realtime Worker → Broker, Cache, Board, Storage

Показать независимое масштабирование Session, Board, Realtime Worker.
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
  Container(auth, "Auth & Accounts Service", "Django/DRF", "JWT, профиль, RBAC")
  Container(social, "Social Service", "Django/DRF", "Друзья, поиск")
  Container(characters, "Character Service", "Django/DRF", "Персонажи, листы")
  Container(session, "Session Service", "Django/DRF", "Комнаты, команды,\nSessionPolicy")
  Container(board, "Board Service", "Django/DRF", "Снапшоты, элементы,\nExcalidrawAdapter")
  Container(dice, "Dice Service", "Django/DRF", "Броски, история")
  Container(adminSvc, "Administration Service", "Django/DRF", "Runtime-настройки")
  Container(worker, "Realtime Worker", "Celery", "Broadcast WSS,\npersist snapshots")
  ContainerDb(db, "Database", "PostgreSQL", "Транзакционные данные")
  ContainerDb(cache, "Cache", "Redis", "Presence, кеш")
  ContainerQueue(broker, "Broker", "Redis Streams", "SessionEventDTO")
  ContainerDb(storage, "Object Storage", "MinIO", "Карты, портреты")
}

Rel(player, gateway, "HTTPS / WSS")
Rel(master, gateway, "HTTPS / WSS")
Rel(admin, gateway, "HTTPS")
Rel(gateway, frontend, "static")
Rel(gateway, auth, "REST")
Rel(gateway, social, "REST")
Rel(gateway, characters, "REST")
Rel(gateway, session, "REST / WSS")
Rel(gateway, board, "REST")
Rel(gateway, dice, "REST")
Rel(gateway, adminSvc, "REST")
Rel(gateway, worker, "internal")
Rel(frontend, session, "WebSocket", "sync")
Rel(session, broker, "publish events")
Rel(broker, worker, "consume")
Rel(worker, cache, "presence")
Rel(board, storage, "S3")
Rel(characters, storage, "S3")
Rel(social, auth, "JWT")
Rel(characters, auth, "owner check")
Rel(session, auth, "JWT")
Rel(auth, db, "SQL")
Rel(social, db, "SQL")
Rel(characters, db, "SQL")
Rel(session, db, "SQL")
Rel(board, db, "SQL")
Rel(dice, db, "SQL")
Rel(adminSvc, db, "SQL")
Rel(worker, db, "SQL")
Rel(worker, storage, "S3")
@enduml
```
