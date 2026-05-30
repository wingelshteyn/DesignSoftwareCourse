# Диаграмма 4. C4 Context: смысловое ядро

## Промпт
Создай C4 Context диаграмму для смыслового ядра ASTROLL "Игровая сессия (VTT)". Пользователи: Мастер и Игрок. Центральная система: "Игровая сессия: комната, доска, права, события". Вокруг покажи поддомены "Учётные записи", "Комнаты и присутствие", "Персонажи и листы", "Хранение досок", "Броски кубов" и внешнюю библиотеку "Excalidraw". Подпиши назначение связей: JWT и профиль, roster, sheetData и токены, снапшоты, события бросков, canvas API.

## PlantUML
```plantuml
@startuml
left to right direction
skinparam componentStyle rectangle

actor "Мастер" as Master
actor "Игрок" as Player
rectangle "Игровая сессия (VTT)\n[Смысловое ядро]\nКомната, синхронная доска,\nправа и игровые события" as Core

rectangle "Учётные записи\n[Generic]" as Accounts
rectangle "Комнаты и присутствие\n[Supporting]" as Rooms
rectangle "Персонажи и листы\n[Supporting]" as Characters
rectangle "Хранение досок\n[Supporting]" as Boards
rectangle "Броски кубов\n[Supporting]" as Dice
cloud "Excalidraw\n[External]" as Excalidraw

Master --> Core : ведёт сессию,\nуправляет правами
Player --> Core : подключается,\nиграет и редактирует
Core --> Accounts : проверяет JWT,\nполучает профиль
Core --> Rooms : получает roster,\nметаданные комнаты
Core --> Characters : использует sheetData,\nтокены персонажей
Core --> Boards : сохраняет/загружает\nснапшоты
Core <--> Dice : публикует и получает\nсобытия бросков
Core --> Excalidraw : ACL к canvas API
@enduml
```
