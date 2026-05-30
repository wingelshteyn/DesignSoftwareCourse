# Диаграмма 2. UML вариантов использования: Мастер

## Промпт
Создай UML use case диаграмму для роли "Мастер" в ASTROLL. Покажи границу системы. Мастер создает комнату, приглашает игроков, управляет участниками, включает режим "только просмотр", исключает игрока, управляет интерактивной доской, сохраняет и загружает снапшоты доски, ведет заметки мастера, управляет персонажами и токенами, инициирует броски и просматривает историю бросков. Используй include/extend там, где действие является обязательной частью или опциональным расширением.

## PlantUML
```plantuml
@startuml
left to right direction
actor "Мастер" as Master
rectangle "ASTROLL" {
  usecase "Создать комнату" as UC_CreateRoom
  usecase "Пригласить игроков" as UC_Invite
  usecase "Управлять участниками" as UC_Members
  usecase "Выдать режим\nтолько просмотр" as UC_Readonly
  usecase "Исключить игрока" as UC_Kick
  usecase "Управлять доской" as UC_Board
  usecase "Добавить карту/изображение" as UC_Image
  usecase "Добавить текст/фигуры" as UC_Drawables
  usecase "Разместить токены персонажей" as UC_Tokens
  usecase "Сохранить снапшот доски" as UC_SaveBoard
  usecase "Загрузить снапшот доски" as UC_LoadBoard
  usecase "Вести заметки мастера" as UC_Notes
  usecase "Управлять персонажами" as UC_Characters
  usecase "Сделать бросок кубов" as UC_Roll
  usecase "Просмотреть историю бросков" as UC_History
  usecase "Завершить сессию" as UC_EndSession
}

Master --> UC_CreateRoom
Master --> UC_Invite
Master --> UC_Members
Master --> UC_Board
Master --> UC_SaveBoard
Master --> UC_LoadBoard
Master --> UC_Notes
Master --> UC_Characters
Master --> UC_Roll
Master --> UC_History
Master --> UC_EndSession

UC_Members <.. UC_Readonly : <<extend>>
UC_Members <.. UC_Kick : <<extend>>
UC_Board <.. UC_Image : <<extend>>
UC_Board <.. UC_Drawables : <<extend>>
UC_Board <.. UC_Tokens : <<extend>>
UC_CreateRoom ..> UC_Invite : <<include>>
UC_SaveBoard ..> UC_Board : <<include>>
UC_LoadBoard ..> UC_Board : <<include>>
@enduml
```
