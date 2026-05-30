# Диаграмма 6. Порождающий паттерн: Фабричный метод

## Промпт
Создай UML class diagram для паттерна "Фабричный метод" в ASTROLL. Контекст: создание элементов интерактивной доски. Абстрактный продукт BoardElement, конкретные продукты TokenElement, ImageElement, TextElement, ShapeElement, DrawingElement. Абстрактная фабрика BoardElementFactory создает BoardElement из BoardActionPayload. Конкретные фабрики создают свои типы элементов. Клиент BoardUpdateBuilder получает payload и registry фабрик, строит доменное обновление доски.

## PlantUML
```plantuml
@startuml
skinparam classAttributeIconSize 0

class BoardActionPayload {
  +type: str
  +room_id: str
  +author_id: int
  +data: dict
}

abstract class BoardElement {
  +id: str
  +room_id: str
  +created_by: int
  +position: Point
  +can_edit(user_id: int): bool
  +to_snapshot(): dict
}

class TokenElement { +character_id: int }
class ImageElement { +image_url: str }
class TextElement { +text: str }
class ShapeElement { +shape_type: str }
class DrawingElement { +points: list[Point] }

abstract class BoardElementFactory {
  +create_element(payload: BoardActionPayload): BoardElement
}
class TokenElementFactory
class ImageElementFactory
class TextElementFactory
class ShapeElementFactory
class DrawingElementFactory

class BoardElementFactoryRegistry {
  -factories: dict
  +get_factory(type: str): BoardElementFactory
  +register(type: str, factory: BoardElementFactory): void
}

class BoardUpdateBuilder {
  -registry: BoardElementFactoryRegistry
  +build(payload: BoardActionPayload): BoardElement
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
@enduml
```
