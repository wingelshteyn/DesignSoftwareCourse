# Диаграмма 13. C4 Containers: защищённая сервисная поставка

## Промпт
Создай C4 Container диаграмму ASTROLL после добавления безопасности и контейнеризации. Пользователи Мастер и Игрок идут через API Gateway/Nginx. Есть Frontend React, Backend Django/DRF или FastAPI как модульный монолит, PostgreSQL, Redis, Object Storage/MinIO для изображений, Worker для фоновых задач и Broker. Gateway выполняет TLS termination, rate limiting и маршрутизацию; Backend выполняет JWT/RBAC и бизнес-логику.

## PlantUML
```plantuml
@startuml
left to right direction
skinparam componentStyle rectangle

actor "Мастер" as Master
actor "Игрок" as Player

node "ASTROLL\n[Software System]" {
  component "API Gateway\n[Container: Nginx]\nTLS, rate limiting,\nмаршрутизация" as Gateway
  component "Frontend\n[Container: React]\nUI доски, персонажей,\nкомнат" as Frontend
  component "Backend\n[Container: Django/DRF]\nмодульный монолит,\nJWT/RBAC, REST/WebSocket" as Backend
  component "Worker\n[Container: Celery]\nфоновые задачи,\nэкспорт, очистка" as Worker
  database "Database\n[Container: PostgreSQL]\nпользователи, комнаты,\nперсонажи, доски" as DB
  database "Broker & Cache\n[Container: Redis]\nкеш, очереди,\npresence" as Redis
  database "Object Storage\n[Container: MinIO]\nаватары, портреты,\nкарты и изображения" as Storage
}

Master --> Gateway
Player --> Gateway
Gateway --> Frontend : статика
Gateway --> Backend : REST/WebSocket
Frontend --> Backend : API + Socket.IO
Backend --> DB
Backend --> Redis
Backend --> Storage
Backend --> Worker : задачи
Worker --> Redis
Worker --> DB
Worker --> Storage
@enduml
```
