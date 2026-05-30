# Диаграмма 18. 4+1: процессное представление

## Промпт
Создай процессное представление ASTROLL. Синхронные HTTP-запросы идут через API Gateway к Auth, Character, Board и Session Service. Реалтайм-события доски и бросков идут через Realtime Gateway. Session Service публикует события в Broker, а Board Worker сохраняет снапшоты в Object Storage и PostgreSQL. Покажи сценарий: игрок подключается к комнате, получает снапшот, двигает токен, событие рассылается всем участникам и сохраняется в журнал.

## PlantUML
```plantuml
@startuml
left to right direction
skinparam componentStyle rectangle

actor "Игрок" as Player
component "API Gateway" as Gateway
component "Realtime Gateway" as Realtime
component "Session Service" as Session
component "Board Service" as Board
component "Character Service" as Characters
queue "Broker" as Broker
component "Board Worker" as Worker
database "PostgreSQL" as DB
database "Object Storage" as Storage

Player --> Gateway : HTTP login,\nget room
Player --> Realtime : WebSocket connect
Gateway --> Session : join room
Session --> Characters : получить токены\nперсонажей
Session --> Board : получить снапшот
Board --> DB
Board --> Storage
Realtime --> Session : move token command
Session --> Broker : SessionEvent
Broker --> Realtime : broadcast event
Realtime --> Player : обновление доски
Broker --> Worker : persist snapshot task
Worker --> DB : журнал событий
Worker --> Storage : снапшот доски
@enduml
```
