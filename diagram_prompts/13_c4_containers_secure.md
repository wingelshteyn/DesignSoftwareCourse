# Диаграмма 13. C4 Containers: безопасная поставка (рисунок 13)

## Назначение
Рисунок 13 отчёта ПР8. C4 **Container** diagram ASTROLL с Gateway, контейнеризацией и изоляцией.

## Эталон (что должно получиться)
- Граница **ASTROLL [Software System]** (пунктир).
- Персоны **Мастер**, **Игрок** (и опционально **Администратор**) → **API Gateway**.
- Контейнеры: **API Gateway [Nginx]**, **Frontend [React]**, **Backend [Django/DRF]**, **Worker [Celery]**, **Database [PostgreSQL]**, **Broker & Cache [Redis]**, **Object Storage [MinIO]**.
- Русские описания в каждом контейнере.
- Стиль C4 Container — как MDT рис. 13.

## Промпт для генерации
```
Нарисуй C4 Container Diagram для ASTROLL с аспектами безопасности (рис. 13 MDT).

System boundary: ASTROLL [Software System].

Persons: Мастер, Игрок, Администратор — все идут в API Gateway.

Containers:
- API Gateway [Nginx] — TLS, rate limiting, маршрутизация, статика
- Frontend [React] — UI доски, персонажей, комнат
- Backend [Django/DRF] — модульный монолит ASTROLL_OLD, JWT/RBAC
- Worker [Celery] — фоновые задачи: экспорт листов, persist snapshots
- Database [PostgreSQL] — пользователи, комнаты, персонажи, доски
- Broker & Cache [Redis] — presence, очереди, кеш ролей
- Object Storage [MinIO] — аватары, портреты, карты

Связи:
Users → Gateway → Frontend, Backend
Frontend → Backend (REST + WebSocket)
Backend → DB, Redis, Storage, Worker
Worker → Redis, DB, Storage
```

## PlantUML (готовая реализация)
```plantuml
@startuml
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Container.puml

LAYOUT_TOP_DOWN()

Person(master, "Мастер", "Ведёт сессию, управляет комнатой")
Person(player, "Игрок", "Играет, редактирует персонажей")
Person(admin, "Администратор", "Управляет пользователями\nи настройками")

System_Boundary(astroll, "ASTROLL") {
  Container(gateway, "API Gateway", "Nginx", "TLS, rate limiting,\nмаршрутизация, статика")
  Container(frontend, "Frontend", "React", "UI доски, персонажей,\nкомнат")
  Container(backend, "Backend", "Django/DRF", "Модульный монолит:\nAccounts, Session, Board...")
  Container(worker, "Worker", "Celery", "Фоновые задачи:\nэкспорт, persist snapshots")
  ContainerDb(db, "Database", "PostgreSQL", "Пользователи, комнаты,\nперсонажи, доски")
  ContainerDb(redis, "Broker & Cache", "Redis", "Presence, очереди,\nкеш ролей")
  ContainerDb(storage, "Object Storage", "MinIO", "Аватары, портреты,\nкарты")
}

Rel(master, gateway, "HTTPS / WSS")
Rel(player, gateway, "HTTPS / WSS")
Rel(admin, gateway, "HTTPS")
Rel(gateway, frontend, "статика")
Rel(gateway, backend, "REST / WebSocket")
Rel(frontend, backend, "API + Socket.IO")
Rel(backend, db, "SQL")
Rel(backend, redis, "cache / pubsub")
Rel(backend, storage, "S3 API")
Rel(backend, worker, "задачи")
Rel(worker, redis, "broker")
Rel(worker, db, "SQL")
Rel(worker, storage, "S3 API")
@enduml
```
