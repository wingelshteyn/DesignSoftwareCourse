# Диаграмма 5. C4 Context: персонажи и листы

## Промпт
Создай C4 Context диаграмму для вспомогательного поддомена ASTROLL "Персонажи и листы". Центральная система хранит, редактирует, импортирует и экспортирует листы персонажей в JSON, поддерживает портреты, многостраничность и автосохранение. Пользователи: Игрок и Мастер. Покажи связи с "Учётные записи" для владельца и JWT, с "Игровая сессия (VTT)" для передачи sheetData, токенов и данных бросков, с "Справочник Энросс" как внешним источником подсказок по стэндам.

## PlantUML
```plantuml
@startuml
left to right direction
skinparam componentStyle rectangle

actor "Игрок" as Player
actor "Мастер" as Master
rectangle "Персонажи и листы\n[Вспомогательный поддомен]\nCRUD персонажей, JSON-лист,\nпортреты, импорт/экспорт,\nавтосохранение" as Characters
rectangle "Учётные записи\n[Generic]" as Accounts
rectangle "Игровая сессия (VTT)\n[Core]" as Session
database "База данных\nперсонажей" as DB
cloud "Справочник Энросс\n[External]" as Guide

Player --> Characters : создаёт и редактирует\nсвоих персонажей
Master --> Characters : помогает готовить\nперсонажей к игре
Characters --> Accounts : проверяет владельца\nи JWT
Characters --> DB : сохраняет sheetData,\nпортреты, версии схем
Characters --> Session : передаёт sheetData,\nтокены, параметры бросков
Characters --> Guide : получает подсказки\nпо стэндам
@enduml
```
