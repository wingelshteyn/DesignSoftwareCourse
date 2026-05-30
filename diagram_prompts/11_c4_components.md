# Диаграмма 11. C4 Components: модульный монолит (рисунок 11)

## Назначение
Рисунок 11 отчёта ПР8. C4 **Component** diagram контейнера **Backend API** (`ASTROLL_OLD`).

## Эталон (что должно получиться)
- Пунктирная граница **[Container: Backend API]**.
- Компоненты — **[Component: Django App]**, голубые прямоугольники C4.
- **Диагональная компоновка** (как MDT): сверху Friends/Characters, центр Game Session, низ Accounts.
- Стрелки зависимостей **без циклов** (ADP).
- Русские описания в каждом компоненте.

## Промпт для генерации
```
Нарисуй C4 Component Diagram для ASTROLL_OLD (модульный монолит Django).

Стиль рис. 11 MDT: Container Boundary «Backend API», компоненты [Component: Django App], голубые блоки, русские описания, диагональный layout.

Компоненты:
- Accounts — регистрация, вход, JWT, профиль, RBACPolicy
- Friends — поиск пользователей, список друзей
- Characters — CRUD персонажей, JSON-листы, CharacterAccessPolicy
- Rooms — roomId, roster, host, readonly
- Board — элементы доски, ExcalidrawSnapshotAdapter, снапшоты
- Dice — броски d20, история в комнате
- Game Session — GameSessionCommandInvoker, SessionPolicy, realtime
- Administration — RuntimeSettings, AdministrationPolicy

Зависимости (стрелки вниз по устойчивости):
Friends → Accounts
Characters → Accounts
Rooms → Accounts
Board → Accounts
Dice → Characters
Game Session → Accounts, Rooms, Characters, Board, Dice
Administration → Accounts

Без циклов. Не показывать БД на этой диаграмме (только компоненты внутри контейнера).
```

## PlantUML (готовая реализация)
```plantuml
@startuml
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Component.puml

LAYOUT_TOP_DOWN()

Container_Boundary(backend, "Backend API", "Container: Django modular monolith") {
  Component(friends, "Friends", "Django App", "Поиск пользователей,\nсписок друзей")
  Component(characters, "Characters", "Django App", "CRUD персонажей,\nJSON-листы, CharacterAccessPolicy")
  Component(rooms, "Rooms", "Django App", "roomId, roster,\nhost, readonly")
  Component(board, "Board", "Django App", "Элементы доски,\nExcalidrawSnapshotAdapter")
  Component(dice, "Dice", "Django App", "Броски d20,\nистория в комнате")
  Component(session, "Game Session", "Django App", "CommandInvoker,\nSessionPolicy, realtime")
  Component(admin, "Administration", "Django App", "RuntimeSettings,\nAdministrationPolicy")
  Component(accounts, "Accounts", "Django App", "Регистрация, JWT,\nпрофиль, RBACPolicy")
}

Rel(friends, accounts, "использует userId")
Rel(characters, accounts, "проверяет владельца")
Rel(rooms, accounts, "идентифицирует участников")
Rel(board, accounts, "авторизация")
Rel(dice, characters, "character_id")
Rel(session, accounts, "JWT, actor_id")
Rel(session, rooms, "Room, host policy")
Rel(session, characters, "sheetData, токены")
Rel(session, board, "BoardSnapshot, команды")
Rel(session, dice, "DiceRollEntry")
Rel(admin, accounts, "RBACPolicy")

Lay_D(friends, session)
Lay_R(board, session)
@enduml
```
