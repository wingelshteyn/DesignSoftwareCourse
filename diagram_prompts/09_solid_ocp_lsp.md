# Диаграмма 9. SOLID: OCP и LSP для элементов доски

## Промпт
Создай UML/C4 Code диаграмму, показывающую применение OCP и LSP в ASTROLL. BoardUpdateBuilder работает только с абстракцией BoardElementFactory и абстрактным продуктом BoardElement. Все элементы доски имеют одинаковый контракт can_edit, to_snapshot, apply_to. Добавление нового типа элемента не требует изменения клиентского кода. Покажи, что TokenElement, ImageElement, TextElement и ShapeElement могут подставляться вместо BoardElement без проверок типа.

## PlantUML
```plantuml
@startuml
skinparam classAttributeIconSize 0

abstract class BoardElement {
  +id: str
  +room_id: str
  +can_edit(user_id: int): bool
  +to_snapshot(): dict
  +apply_to(board: BoardSnapshot): void
}

class TokenElement
class ImageElement
class TextElement
class ShapeElement

abstract class BoardElementFactory {
  +create_element(payload: BoardActionPayload): BoardElement
}

class TokenElementFactory
class ImageElementFactory
class TextElementFactory
class ShapeElementFactory

class BoardUpdateBuilder {
  -registry: BoardElementFactoryRegistry
  +build(payload: BoardActionPayload): BoardElement
}

class BoardElementFactoryRegistry {
  +get_factory(type: str): BoardElementFactory
  +register(type: str, factory: BoardElementFactory): void
}

BoardElement <|-- TokenElement
BoardElement <|-- ImageElement
BoardElement <|-- TextElement
BoardElement <|-- ShapeElement

BoardElementFactory <|-- TokenElementFactory
BoardElementFactory <|-- ImageElementFactory
BoardElementFactory <|-- TextElementFactory
BoardElementFactory <|-- ShapeElementFactory

BoardUpdateBuilder --> BoardElementFactoryRegistry
BoardElementFactoryRegistry --> BoardElementFactory
BoardElementFactory ..> BoardElement

note right of BoardElement
LSP: любой конкретный элемент
используется как BoardElement
без ветвления по типу.
end note

note bottom of BoardElementFactory
OCP: новый тип элемента добавляется
новой фабрикой и регистрацией,
без изменения BoardUpdateBuilder.
end note
@enduml
```
