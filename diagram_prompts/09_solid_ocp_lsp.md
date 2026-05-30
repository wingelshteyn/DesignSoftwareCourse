# Диаграмма 9. SOLID: OCP и LSP (рисунок 9)

## Назначение
Рисунок 9 отчёта ПР8. UML после исправления **LSP**: все элементы доски имеют **единый контракт** `BoardElement`.

## Эталон (что должно получиться)
- Как рис. 6, но **все подклассы BoardElement** реализуют **одинаковые методы** (`can_edit`, `to_snapshot`) — **без «особых» методов** у отдельных типов.
- **BoardUpdateBuilder** не делает `isinstance` — работает только через `BoardElementFactory` и `BoardElement`.
- Жёлтые классы; примечания OCP/LSP справа (optional note).
- Отражает `board/elements.py` после рефакторинга LSP.

## Промпт для генерации
```
Нарисуй UML Class Diagram для ASTROLL, демонстрирующий OCP и LSP (рис. 9 MDT).

Контекст: фабрика элементов доски. Все конкретные элементы (Token, Image, Text, Shape, Drawing) — полноценные подтипы BoardElement с ОДИНАКОВЫМ контрактом:
- can_edit(user_id: int): bool
- to_snapshot(): dict

Никаких дополнительных публичных методов только у одного подтипа (исправление LSP).

OCP: BoardUpdateBuilder и BoardElementFactoryRegistry не меняются при добавлении нового типа — достаточно новой фабрики и register().

Покажи:
abstract BoardElement + 5 подклассов
abstract BoardElementFactory + 5 фабрик
BoardElementFactoryRegistry, BoardUpdateBuilder

Builder.build() возвращает BoardElement — клиент не знает конкретный тип.

Добавь note: «LSP: любой элемент подставляется как BoardElement» и «OCP: расширение через новую фабрику».
```

## PlantUML (готовая реализация)
```plantuml
@startuml
skinparam classAttributeIconSize 0
skinparam class {
  BackgroundColor #FEFECE
  BorderColor black
}

abstract class BoardElement {
  +element_id: str
  +room_id: str
  +created_by: int
  +can_edit(user_id: int): bool
  +to_snapshot(): dict
}

class TokenElement
class ImageElement
class TextElement
class ShapeElement
class DrawingElement

abstract class BoardElementFactory {
  +create_element(payload: BoardActionPayload): BoardElement
}

class TokenElementFactory
class ImageElementFactory
class TextElementFactory
class ShapeElementFactory
class DrawingElementFactory

class BoardElementFactoryRegistry {
  +register(type: str, factory: BoardElementFactory): void
  +get_factory(type: str): BoardElementFactory
}

class BoardUpdateBuilder {
  -_registry: BoardElementFactoryRegistry
  +build(payload: BoardActionPayload): BoardElement
}

class BoardActionPayload {
  +element_type: str
  +data: dict
}

BoardElement <|-- TokenElement
BoardElement <|-- ImageElement
BoardElement <|-- TextElement
BoardElement <|-- ShapeElement
BoardElement <|-- DrawingElement

BoardElementFactory <|-- TokenElementFactory
BoardElementFactory <|-- ImageElementFactory
BoardElementFactory <|-- TextElementFactory
BoardElementFactory <|-- ShapeElementFactory
BoardElementFactory <|-- DrawingElementFactory

BoardUpdateBuilder --> BoardElementFactoryRegistry
BoardElementFactoryRegistry --> BoardElementFactory
BoardElementFactory ..> BoardElement
BoardElementFactory ..> BoardActionPayload

note right of BoardElement
LSP: TokenElement, ImageElement и др.
подставляются как BoardElement
без проверки типа.
end note

note bottom of BoardElementFactory
OCP: новый тип = новая фабрика + register(),
BoardUpdateBuilder не меняется.
end note
@enduml
```
