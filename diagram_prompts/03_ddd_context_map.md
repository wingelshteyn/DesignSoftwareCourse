# Диаграмма 3. DDD карта контекстов

## Промпт
Создай DDD context map для ASTROLL. В центре смысловое ядро "Game Session / VTT": комната, синхронная доска, присутствие участников, права мастера и игровые события. Покажи контексты Accounts, Friends, Characters, Board Storage, Rooms, Dice и внешний Excalidraw. Отметь типы отношений: Conformist от доменных контекстов к Accounts, Customer-Supplier от Characters/Board Storage/Rooms к Game Session, Partnership между Game Session и Dice, Anti-Corruption Layer между Game Session и Excalidraw. Подпиши Upstream/Downstream.

## PlantUML
```plantuml
@startuml
left to right direction
skinparam componentStyle rectangle

component "Accounts\n[Generic]\nПользователи, JWT,\nпрофили" as Accounts
component "Friends\n[Supporting]\nДрузья и поиск" as Friends
component "Characters\n[Supporting]\nЛисты персонажей,\nпортреты, JSON" as Characters
component "Board Storage\n[Supporting]\nСнапшоты досок" as Boards
component "Rooms\n[Supporting]\nroomId, roster,\nприглашения" as Rooms
component "Dice\n[Supporting]\nБроски и история" as Dice
component "Game Session / VTT\n[Core]\nРеалтайм-доска,\nправа, события" as Session
cloud "Excalidraw\n[External]" as Excalidraw

Friends ..> Accounts : Conformist\nD -> U
Characters ..> Accounts : Conformist\nD -> U
Rooms ..> Accounts : Conformist\nD -> U
Session ..> Accounts : Conformist\nD -> U

Session ..> Characters : Customer-Supplier\nD -> U
Session ..> Boards : Customer-Supplier\nD -> U
Session ..> Rooms : Customer-Supplier\nD -> U
Session -- Dice : Partnership
Session ..> Excalidraw : ACL\nадаптация canvas API
@enduml
```
