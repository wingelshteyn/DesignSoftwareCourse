# Диаграмма 20. 4+1: физическое представление

## Промпт
Создай physical/deployment view ASTROLL. Пользователи и браузеры подключаются к Gateway Node. Внутри Kubernetes Cluster несколько application nodes с контейнерами frontend, api gateway, auth, session, realtime, board, characters, dice, workers. Отдельно покажи Primary PostgreSQL и Replica PostgreSQL, Redis Cluster/Broker, Object Storage Node и Storage Replica. Gateway принимает HTTPS/WebSocket. Сервисы масштабируются горизонтально.

## PlantUML
```plantuml
@startuml
left to right direction

node "User Devices\nBrowser" as Browser
node "Gateway Node\nHTTPS / WebSocket" as Gateway

node "K8s Cluster\nApplication Nodes" as K8s {
  node "Pod: Frontend" as Frontend
  node "Pod: API Gateway" as ApiGateway
  node "Pods: Auth Service" as Auth
  node "Pods: Session Service" as Session
  node "Pods: Realtime Gateway" as Realtime
  node "Pods: Board Service" as Board
  node "Pods: Character Service" as Characters
  node "Pods: Dice Service" as Dice
  node "Pods: Workers" as Workers
}

database "Primary PostgreSQL\nServer" as PgPrimary
database "Replica PostgreSQL\nServer" as PgReplica
database "Redis Cluster\nCache/Broker" as Redis
database "S3 Node\nObject Storage" as S3
database "S3 Replica\nBackup Storage" as S3Replica

Browser --> Gateway
Gateway --> ApiGateway
ApiGateway --> Frontend
ApiGateway --> Auth
ApiGateway --> Session
ApiGateway --> Board
ApiGateway --> Characters
ApiGateway --> Dice
ApiGateway --> Realtime
Session --> Redis
Realtime --> Redis
Workers --> Redis
Auth --> PgPrimary
Session --> PgPrimary
Board --> PgPrimary
Characters --> PgPrimary
Dice --> PgPrimary
PgPrimary --> PgReplica
Board --> S3
Characters --> S3
S3 --> S3Replica
@enduml
```
