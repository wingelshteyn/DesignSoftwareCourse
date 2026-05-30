# Диаграмма 12. C4 Components: безопасность (рисунок 12)

## Назначение
Рисунок 12 отчёта ПР8. Обновлённая C4 Component diagram с выделенным **Authorization**.

## Эталон (что должно получиться)
- Как рис. 11, но добавлен компонент **Authorization** [Component: Django App].
- **Accounts** — только аутентификация (без RBAC-проверок в каждом модуле).
- Все защищённые компоненты → **Authorization** → **Accounts**.
- Layout: Authorization между Session и Accounts (как в MDT).

## Промпт для генерации
```
Нарисуй обновлённую C4 Component Diagram ASTROLL после усиления безопасности (рис. 12 MDT).

Container «Backend API», компоненты [Component: Django App].

Компоненты:
- Accounts — регистрация, аутентификация, bcrypt, JWT, профиль (БЕЗ проверки прав в каждом запросе)
- Authorization — RBACPolicy, SessionPolicy, CharacterAccessPolicy, проверка прав комнаты и владельца
- Friends, Characters, Board, Rooms, Dice, Game Session, Administration — как в монолите

Зависимости:
- Authorization → Accounts (получает роль/userId)
- Friends, Characters, Board, Rooms, Dice, Game Session, Administration → Authorization
- Administration → Accounts
- Game Session → Rooms, Board, Dice, Characters (доменные связи сохраняются)

Показать, что каждый защищённый компонент сначала обращается к Authorization.
```

## PlantUML (готовая реализация)
```plantuml
@startuml
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Component.puml

LAYOUT_TOP_DOWN()

Container_Boundary(backend, "Backend API", "Container: Django modular monolith") {
  Component(friends, "Friends", "Django App", "Социальные связи,\nпоиск пользователей")
  Component(characters, "Characters", "Django App", "Персонажи и листы")
  Component(rooms, "Rooms", "Django App", "Комнаты и roster")
  Component(board, "Board", "Django App", "Снапshоты и элементы доски")
  Component(dice, "Dice", "Django App", "Броски и история")
  Component(session, "Game Session", "Django App", "Команды сессии,\nreadonly/kick")
  Component(admin, "Administration", "Django App", "Runtime-настройки")
  Component(authz, "Authorization", "Django App", "RBAC, SessionPolicy,\nCharacterAccessPolicy")
  Component(accounts, "Accounts", "Django App", "Регистрация,\nаутентификация, JWT")
}

Rel(friends, authz, "проверка доступа")
Rel(characters, authz, "CharacterAccessPolicy")
Rel(board, authz, "права редактирования")
Rel(rooms, authz, "host / member")
Rel(dice, authz, "участник комнаты")
Rel(session, authz, "SessionPolicy")
Rel(admin, authz, "can_administer")
Rel(authz, accounts, "роль, userId")
Rel(session, rooms, "Room aggregate")
Rel(session, board, "BoardSnapshot")
Rel(session, dice, "DiceRollEntry")
Rel(session, characters, "sheetData")
Rel(admin, accounts, "управление пользователями")
@enduml
```
