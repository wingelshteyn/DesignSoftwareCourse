# Диаграмма 12. C4 Components: безопасность

## Промпт
Создай обновлённую C4 Component диаграмму ASTROLL после добавления аспектов безопасности. Вынеси Authorization как отдельный компонент проверки прав и политик доступа. Покажи Auth & Accounts, Friends, Characters, Board, Rooms, Game Session, Dice, Audit, Input Validation, Encryption/Secrets. Все защищённые компоненты используют Authorization. Audit получает события команд, а Encryption/Secrets используется для JWT secret, хеширования паролей и приватных данных.

## PlantUML
```plantuml
@startuml
left to right direction
skinparam componentStyle rectangle

package "Backend API\n[Container]" {
  component "Auth & Accounts\nлогин, bcrypt,\nJWT, профиль" as Accounts
  component "Authorization\nRBAC/ABAC,\nправа комнаты,\nпроверка владельца" as Authz
  component "Input Validation\nDTO/Zod/Pydantic,\n4xx ошибки" as Validation
  component "Characters\nперсонажи и листы" as Characters
  component "Board\nснапшоты досок" as Board
  component "Rooms\nкомнаты и участники" as Rooms
  component "Game Session\nкоманды сессии,\nreadonly/kick" as Session
  component "Dice\nброски" as Dice
  component "Friends\nдрузья" as Friends
  component "Audit\nжурнал действий" as Audit
  component "Encryption & Secrets\nJWT secret,\nпароли, приватные поля" as Crypto
}

database "PostgreSQL" as DB

Accounts --> Crypto
Accounts --> Validation
Authz --> Accounts
Characters --> Authz
Characters --> Validation
Board --> Authz
Board --> Validation
Rooms --> Authz
Session --> Authz
Session --> Validation
Session --> Audit
Dice --> Authz
Friends --> Authz
Audit --> DB
Accounts --> DB
Characters --> DB
Board --> DB
Rooms --> DB
Session --> DB
Dice --> DB
Friends --> DB
@enduml
```
