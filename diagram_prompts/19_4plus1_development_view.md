# Диаграмма 19. 4+1: представление уровня разработки (рисунок 19)

## Назначение
Рисунок 19 отчёта ПР8. **Development View** — структура репозитория и слоёв сервисов.

## Эталон (что должно получиться)
- **Session Service** (шаблон) — внутри 4 блока: **api**, **service**, **repository**, **models**; realtime-worker входит в слой service.
- **Board Service** — **api**, **app** (или service).
- **shared-contracts** снизу по центру: **DTOs**, **Interfaces**.
- Прямоугольники с тенью, layout треугольник как в MDT.
- Путь: `ASTROLL/services/*`, `ASTROLL/shared-contracts/`.

## Промпт для генерации
```
Нарисуй Development View (4+1) для ASTROLL, стиль рис. 19 MDT.

Три блока:

1. Session Service (общий шаблон сервисов) — большой прямоугольник с подписью «(общий шаблон сервисов)», внутри 4 ячейки:
   - api (FastAPI/uvicorn endpoints)
   - service (commands, policies)
   - repository (persistence)
   - models (domain)

2. Board Service — прямоугольник с api + service (excalidraw_adapter, board_elements)

3. shared-contracts — внизу по центру, внутри:
   - DTOs (UserRef, BoardSnapshotDTO, SessionEventDTO, DiceRollDTO)
   - Interfaces (контракты между сервисами)

Связи: Session Service и Board Service зависят от shared-contracts (стрелки вниз).

Также упомянуть в промпте: у каждого из 6 сервисов (`identity`, `characters`, `session`, `board`, `dice`, `administration`) есть Dockerfile, ci.yml, requirements.txt, tests/.
```

## PlantUML (готовая реализация)
```plantuml
@startuml
skinparam rectangle {
  BackgroundColor white
  BorderColor black
  shadowing true
}
skinparam packageStyle rectangle

rectangle "Session Service\n(общий шаблон сервисов)" as Session {
  rectangle "api" as s_api
  rectangle "service\n(commands, policies,\nrealtime worker)" as s_svc
  rectangle "repository" as s_repo
  rectangle "models" as s_mod
}

rectangle "Board Service" as Board {
  rectangle "api" as b_api
  rectangle "service\n(board_elements,\nexcalidraw_adapter)" as b_svc
}

rectangle "shared-contracts" as Contracts {
  rectangle "DTOs\nUserRef, BoardSnapshotDTO,\nSessionEventDTO, DiceRollDTO" as DTOs
  rectangle "Interfaces\nконтракты между сервисами" as IF
}

Session -[hidden]left- Board
Session -[hidden]down- Contracts
Board -[hidden]down- Contracts

Session --> Contracts : import DTOs
Board --> Contracts : import DTOs

note bottom of Session
  ASTROLL/services/session/
  + Dockerfile, ci.yml, tests/
end note

note bottom of Contracts
  ASTROLL/shared-contracts/python/
  astroll_shared_contracts/contracts.py
end note
@enduml
```
