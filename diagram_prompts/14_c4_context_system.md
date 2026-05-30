# Диаграмма 14. C4 Context: система ASTROLL

## Промпт
Создай C4 Context диаграмму всей системы ASTROLL. Персоны: Игрок, Мастер, Администратор. Центральная система: ASTROLL - веб-платформа для проведения онлайн настольных ролевых игр. Игрок хранит персонажей, подключается к комнатам, делает броски и взаимодействует с доской. Мастер создает и ведет комнаты, управляет участниками, сценами и снапшотами. Администратор управляет пользователями и эксплуатационными параметрами. Внешние системы: Email/Notification Service для уведомлений, Object Storage для медиа, Excalidraw как библиотека доски.

## PlantUML
```plantuml
@startuml
left to right direction

actor "Игрок" as Player
actor "Мастер" as Master
actor "Администратор" as Admin

rectangle "ASTROLL\n[Software System]\nОнлайн VTT: комнаты,\nдоски, персонажи,\nброски и друзья" as Astroll
cloud "Email/Notification Service\n[External]" as Notify
cloud "Object Storage\n[External]" as Storage
cloud "Excalidraw\n[External Library]" as Excalidraw

Player --> Astroll : хранит персонажей,\nиграет в комнате,\nделает броски
Master --> Astroll : ведёт сессию,\nуправляет участниками,\nсохраняет доски
Admin --> Astroll : управляет пользователями,\nнастройками и аудитом
Astroll --> Notify : отправляет приглашения\nи уведомления
Astroll --> Storage : хранит карты,\nпортреты, аватары
Astroll --> Excalidraw : использует canvas API\nчерез адаптер
@enduml
```
