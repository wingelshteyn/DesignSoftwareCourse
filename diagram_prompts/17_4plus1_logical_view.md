# Диаграмма 17. 4+1: логическое представление (рисунок 17)

## Назначение
Рисунок 17 отчёта ПР8. **Логическое представление** — облачная DDD-диаграмма связей сущностей и сервисов (не UML class diagram).

## Эталон (что должно получиться)
- **Облачные формы** (cloud) с **пунктирной границей**.
- Узлы-сущности: SessionEvent, BoardSnapshot, DiceRoll, RoomRef, CharacterRef и т.д.
- Узлы-сервисы: Session Service, Board Service, Auth Service...
- Связи с маркерами **○** (open circle) и **●** (filled circle) как в MDT.
- Стиль: белый фон, чёрный текст, layout сверху вниз.

## Промпт для генерации
```
Нарисуй Logical View (4+1) для ASTROLL после реструктуризации, стиль рис. 17 MDT.

НЕ UML class diagram. Используй cloud-узлы с пунктирной границей.

Сущности (cloud):
- SessionEvent — room_id, event_type, payload
- BoardSnapshot — board_id, version, elements
- BoardElement — element_id, type
- DiceRoll — room_id, formula, total
- RoomRef — room_id, host_id
- CharacterRef — character_id, owner_id
- UserRef — user_id, nickname

Сервисы (cloud, крупнее):
- Session Service
- Board Service
- Character Service
- Dice Service
- Auth & Accounts Service
- Realtime Worker

Связи (со маркерами):
- Session Service ○-- SessionEvent (создаёт)
- Session Service ○-- RoomRef (управляет)
- Session Service ○-- CharacterRef (использует токены)
- Board Service ●-- BoardSnapshot (владеет)
- BoardSnapshot ●-- BoardElement (содержит)
- Dice Service ●-- DiceRoll
- Session Service ○-- DiceRoll (публикует)
- Character Service ●-- CharacterRef
- Auth Service ●-- UserRef
- Realtime Worker ○-- SessionEvent (рассылает)

Layout: сервисы в центре, сущности вокруг, стрелки с подписями.
```

## PlantUML (готовая реализация)
```plantuml
@startuml
skinparam cloud {
  BackgroundColor white
  BorderColor black
  BorderStyle dashed
  shadowing true
}
skinparam arrow Color black

cloud "Session Service" as SS
cloud "Board Service" as BS
cloud "Character Service" as CS
cloud "Dice Service" as DS
cloud "Auth & Accounts Service" as AS
cloud "Realtime Worker" as RW

cloud "SessionEvent\nroom_id, event_type,\npayload" as SE
cloud "BoardSnapshot\nboard_id, version" as Snap
cloud "BoardElement\nelement_id, type" as BE
cloud "DiceRoll\nformula, total" as DR
cloud "RoomRef\nroom_id, host_id" as RR
cloud "CharacterRef\ncharacter_id, owner_id" as CR
cloud "UserRef\nuser_id, nickname" as UR

SS o-- SE : создаёт
SS o-- RR : управляет
SS o-- CR : токены
SS o-- DR : публикует
BS *-- Snap : владеет
Snap *-- BE : содержит
DS *-- DR : формирует
CS *-- CR : владеет
AS *-- UR : владеет
RW o-- SE : рассылает

SS -[hidden]down- BS
CS -[hidden]left- SS
DS -[hidden]right- SS
AS -[hidden]left- CS
RW -[hidden]right- BS
@enduml
```
