# Диаграмма 4. C4 Context: смысловое ядро (рисунок 4)

## Назначение
Рисунок 4 отчёта ПР8. C4 Context для **смыслового ядра** «Игровая сессия (VTT)».

## Эталон (что должно получиться)
- Нотация **C4 Context** (тёмно-синие блоки Person/System, белый текст).
- **Мастер** и **Игрок** — персоны сверху/сбоку.
- Центр: **«Игровая сессия (VTT)»** [Software System / Core].
- Вокруг — смежные подсистемы как **Software System** или **External System**.
- Стрелки с **русскими подписями** назначения связи.
- Внешняя система **Excalidraw** — облако/External.

## Промпт для генерации
```
Нарисуй C4 Context Diagram для смыслового ядра ASTROLL «Игровая сессия (VTT)».

Стиль C4: тёмно-синие прямоугольники, Person с иконкой человека, подписи [Person]/[Software System]/[External System], русские описания на стрелках.

Персоны:
- Мастер — ведёт сессию, управляет правами, сохраняет доски
- Игрок — подключается к комнате, редактирует доску при наличии прав, делает броски

Центральная система:
- Игровая сессия (VTT) [Software System] — комната, синхронная доска, права, игровые события

Смежные системы:
- Учётные записи [Software System] — JWT, профиль, userId
- Комнаты и присутствие [Software System] — roomId, roster, host
- Персонажи и листы [Software System] — sheetData, токены
- Хранение досок [Software System] — снапshоты Excalidraw
- Броски кубов [Software System] — roll:entry, история
- Excalidraw [External System] — canvas API

Связи:
- Мастер → Игровая сессия: ведёт сессию, readonly/kick
- Игрок → Игровая сессия: играет, редактирует доску
- Игровая сессия → Учётные записи: проверяет JWT
- Игровая сессия → Комнаты: roster, host
- Игровая сессия → Персонажи: sheetData, токены
- Игровая сессия → Хранение досок: save/load snapshot
- Игровая сессия ↔ Броски: события бросков
- Игровая сессия → Excalidraw: ACL, canvas API
```

## PlantUML (готовая реализация)
```plantuml
@startuml
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Context.puml

LAYOUT_WITH_LEGEND()
LAYOUT_TOP_DOWN()

Person(master, "Мастер", "Ведёт сессию, управляет правами,\nсохраняет и загружает доски")
Person(player, "Игрок", "Подключается к комнате,\nредактирует доску, делает броски")

System(core, "Игровая сессия (VTT)", "Комната, синхронная доска,\nправа мастера, игровые события")
System(accounts, "Учётные записи", "JWT, профиль, userId")
System(rooms, "Комнаты и присутствие", "roomId, roster, host")
System(characters, "Персонажи и листы", "sheetData, токены персонажей")
System(boards, "Хранение досок", "Снапшоты Excalidraw в БД")
System(dice, "Броски кубов", "roll:entry, история бросков")
System_Ext(excalidraw, "Excalidraw", "Библиотека canvas для отрисовки доски")

Rel(master, core, "Ведёт сессию,\nreadonly/kick")
Rel(player, core, "Играет,\nредактирует доску")
Rel(core, accounts, "Проверяет JWT,\nполучает профиль")
Rel(core, rooms, "Roster,\nметаданные комнаты")
Rel(core, characters, "sheetData,\nтокены")
Rel(core, boards, "Save/load\nsnapshot")
Rel(core, dice, "Публикует и получает\nсобытия бросков", "sync")
Rel(core, excalidraw, "ACL к canvas API")
@enduml
```
