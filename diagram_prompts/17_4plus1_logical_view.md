# Диаграмма 17. 4+1: логическое представление

## Промпт
Создай логическое представление архитектуры ASTROLL после реструктуризации. Покажи основные доменные сервисы и сущности: Auth & Accounts Service, Character Service, Session Service, Board Service, Dice Service. Сущности: User, Character, Room, RoomMember, BoardSnapshot, BoardElement, DiceRollEntry, SessionEvent. Связи: пользователь владеет персонажами, комната содержит участников, сессия управляет доской и событиями, броски связаны с персонажем и комнатой.

## PlantUML
```plantuml
@startuml
skinparam classAttributeIconSize 0

class User { +id: int; +login: str; +nickname: str }
class Character { +id: int; +owner_id: int; +name: str; +sheet_data: dict }
class Room { +id: str; +host_id: int; +title: str }
class RoomMember { +room_id: str; +user_id: int; +readonly: bool }
class BoardSnapshot { +id: int; +room_id: str; +version: int; +snapshot: dict }
abstract class BoardElement { +id: str; +type: str; +position: Point }
class TokenElement { +character_id: int }
class ImageElement { +url: str }
class DiceRollEntry { +room_id: str; +character_id: int; +formula: str; +total: int }
class SessionEvent { +room_id: str; +type: str; +payload: dict }

class AuthAccountsService { +authenticate(login: str, password: str): Token }
class CharacterService { +get_sheet(character_id: int): Character }
class SessionService { +execute(command: GameSessionCommand): SessionEvent }
class BoardService { +save_snapshot(snapshot: BoardSnapshot): void }
class DiceService { +roll(character_id: int, formula: str): DiceRollEntry }

User "1" -- "many" Character
Room "1" -- "many" RoomMember
User "1" -- "many" RoomMember
Room "1" -- "many" BoardSnapshot
BoardSnapshot "1" -- "many" BoardElement
BoardElement <|-- TokenElement
BoardElement <|-- ImageElement
Room "1" -- "many" DiceRollEntry
Character "1" -- "many" DiceRollEntry
Room "1" -- "many" SessionEvent

SessionService --> AuthAccountsService
SessionService --> CharacterService
SessionService --> BoardService
SessionService --> DiceService
@enduml
```
