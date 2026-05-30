# Диаграмма 11. C4 Components: модульный монолит ASTROLL

## Промпт
Создай C4 Component диаграмму backend ASTROLL как модульного монолита. Контейнер "Backend API" содержит компоненты: Accounts, Friends, Characters, Rooms, Board, Dice, Game Session, Administration. Покажи зависимости без циклов: Game Session зависит от Accounts, Rooms, Characters, Board и Dice; Friends зависит от Accounts; Characters зависит от Accounts; Board зависит от Accounts; Administration зависит от Accounts и Game Session. Общая БД используется через репозитории модулей.

## PlantUML
```plantuml
@startuml
left to right direction
skinparam componentStyle rectangle

package "Backend API\n[Container: modular monolith]" {
  component "Accounts\nрегистрация, JWT,\nпрофиль" as Accounts
  component "Friends\nпоиск и друзья" as Friends
  component "Characters\nлисты персонажей" as Characters
  component "Rooms\nroomId, roster,\nправа участника" as Rooms
  component "Board\nснапшоты и элементы" as Board
  component "Dice\nброски и история" as Dice
  component "Game Session\nреалтайм-сессия,\nкоманды, права" as Session
  component "Administration\nпараметры комнат,\nмодерация" as Admin
}

database "PostgreSQL\nобщая БД монолита" as DB

Friends --> Accounts
Characters --> Accounts
Rooms --> Accounts
Board --> Accounts
Dice --> Characters
Session --> Accounts
Session --> Rooms
Session --> Characters
Session --> Board
Session --> Dice
Admin --> Accounts
Admin --> Session

Accounts --> DB
Friends --> DB
Characters --> DB
Rooms --> DB
Board --> DB
Dice --> DB
Session --> DB
Admin --> DB
@enduml
```
