# Диаграмма 20. 4+1: физическое представление (рисунок 20)

## Назначение
Рисунок 20 отчёта ПР8. **Physical/Deployment View** — Docker/K8s развёртывание.

## Эталон (что должно получиться)
- **Player Browser** и **Master Browser** сверху (вместо Camera + Operator в MDT).
- **Gateway Node** — единая точка входа HTTPS/WSS.
- **K8s Nodes** — стопка квадратов (несколько pod'ов).
- **Primary PostgreSQL → Replica PostgreSQL** (репликация).
- **S3 Node → S3 Replica** (реплика хранилища).
- Чёрно-белый deployment-стиль как MDT рис. 20.
- Источник: `ASTROLL/docker-compose.yml`.

## Промпт для генерации
```
Нарисуй Physical/Deployment View (4+1) для ASTROLL, стиль рис. 20 MDT.

Сверху external nodes:
- Player Browser — браузер игрока
- Master Browser — браузер мастера
Оба → Gateway Node (HTTPS / WebSocket)

Gateway Node → K8s Nodes (стопка из 3 квадратов, подпись «Services & Worker»):
  Pods: Frontend, API Gateway, identity, session, board, characters, dice, administration
  Note: всего 6 backend-сервисов; realtime-worker входит в pod/deployment `session`.

Справа storage tier (два ряда):
- Primary Database Server → Replica Database Server (PostgreSQL)
- S3 Node (MinIO) → S3 Replica Server

K8s → Primary DB, K8s → S3 Node
Self-loop на K8s (внутренняя коммуникация сервисов)

Подписи на русском. Чёрно-белая deployment diagram.
```

## PlantUML (готовая реализация)
```plantuml
@startuml
skinparam nodesep 30
skinparam ranksep 40

node "Player Browser" as PB
node "Master Browser" as MB
node "Gateway Node\nHTTPS / WebSocket" as GW

node "K8s Nodes\n(Services & Worker)" as K8s {
  node "Pods" as Pods {
    artifact "Frontend"
    artifact "API Gateway"
    artifact "identity"
    artifact "session"
    artifact "board"
    artifact "characters"
    artifact "dice"
    artifact "administration"
  }
}

database "Primary Database\nServer\n[PostgreSQL]" as PG1
database "Replica Database\nServer" as PG2
database "S3 Node\n[MinIO]" as S3
database "S3 Replica\nServer" as S3R

PB --> GW
MB --> GW
GW --> K8s
K8s --> PG1 : SQL
PG1 --> PG2 : replication
K8s --> S3 : object API
S3 --> S3R : replication
K8s --> K8s : inter-service\nHTTP / Redis

note right of K8s
  docker-compose.yml /
  Kubernetes horizontal
  scaling: session, board;
  6 backend services;
  realtime-worker inside session
end note
@enduml
```
