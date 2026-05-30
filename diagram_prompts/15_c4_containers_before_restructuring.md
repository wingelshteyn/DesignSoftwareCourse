# Диаграмма 15. C4 Containers: до реструктуризации (рисунок 15)

## Назначение
Рисунок 15 отчёта ПР8. C4 Container diagram **ASTROLL_OLD** (модульный монолит).

## Эталон (что должно получиться)
- Как MDT рис. 15: **один Backend-контейнер** содержит всю бизнес-логику.
- **API Gateway**, **Frontend**, **Backend [Django/DRF]**, **Worker**, **PostgreSQL**, **Redis**, **MinIO**.
- Примечание: backend масштабируется **целиком**.
- Без отдельных микросервисов.

## Промпт для генерации
```
Нарисуй C4 Container Diagram ASTROLL ДО реструктуризации (рис. 15 MDT) — ASTROLL_OLD.

Persons: Игрок, Мастер → API Gateway.

Containers внутри ASTROLL:
- API Gateway [Nginx]
- Frontend [React]
- Backend [Django/DRF] — модульный монолит: Accounts, Friends, Characters, Rooms, Board, Dice, Game Session, Administration (всё в одном deploy)
- Worker [Celery] — фоновые задачи realtime/persist
- Database [PostgreSQL]
- Broker & Cache [Redis]
- Object Storage [MinIO]

Связи как в MDT monolith: Gateway→Frontend, Gateway→Backend, Backend→DB/Redis/Storage/Worker.

Note на Backend: «Один контейнер — весь домен; масштабируется целиком».
```

## PlantUML (готовая реализация)
```plantuml
@startuml
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Container.puml

LAYOUT_TOP_DOWN()

Person(player, "Игрок", "Подключается к комнате")
Person(master, "Мастер", "Ведёт сессию")

System_Boundary(astroll, "ASTROLL до реструктуризации") {
  Container(gateway, "API Gateway", "Nginx", "Обратный прокси,\nrate limiting")
  Container(frontend, "Frontend", "React", "UI VTT, персонажей")
  Container(backend, "Backend", "Django/DRF", "Модульный монолит:\nAccounts, Friends, Characters,\nRooms, Board, Dice, Game Session")
  Container(worker, "Worker", "Celery", "Фоновые задачи,\npersist snapshots")
  ContainerDb(db, "Database", "PostgreSQL", "Единая БД монолита")
  ContainerDb(redis, "Broker & Cache", "Redis", "Presence, очереди")
  ContainerDb(storage, "Object Storage", "MinIO", "Медиа и снапшоты")
}

Rel(player, gateway, "HTTPS / WSS")
Rel(master, gateway, "HTTPS / WSS")
Rel(gateway, frontend, "статика")
Rel(gateway, backend, "REST / WebSocket")
Rel(frontend, backend, "API")
Rel(backend, db, "SQL")
Rel(backend, redis, "pub/sub")
Rel(backend, storage, "S3")
Rel(backend, worker, "tasks")
Rel(worker, redis, "broker")
Rel(worker, db, "SQL")

note right of backend
  Один backend-контейнер содержит
  все модули ASTROLL_OLD и
  масштабируется целиком.
end note
@enduml
```
